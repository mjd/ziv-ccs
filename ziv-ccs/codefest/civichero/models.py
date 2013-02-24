from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

import LocationUtils

from fields import CurrencyField


class CivicType(models.Model):
    avatar = models.ImageField(upload_to='uploads')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return str(self.name)



class Location(models.Model):
    """Abstract base class for anything with an address.  This model stores the address information and also the geo
    coordinates of a place."""
    place_name = models.CharField(max_length=600)
    street_address = models.CharField(max_length=600)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=30)
    lat = models.CharField(max_length=50, blank=True, editable=False)
    lon = models.CharField(max_length=50, blank=True, editable=False)

    def __unicode__(self):

        return self.address()

    def address(self):
        """"Get the address of in standard format: street address city, STATE zip"""
        return self.street_address + ' ' + self.city + ', ' + self.state + ' ' + self.zip_code

    def save(self, force_insert=False, force_update=False, using=None):
        """Overridden to update the Lat and lon on save."""

        LocationUtils.updateGeo(self)
        super(Location, self).save(force_insert, force_update, using)


class CivicProfile(models.Model):

    user = models.ForeignKey(User, unique=True)
    avatar = models.ImageField(upload_to='uploads')


class Citizen(CivicProfile):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 50)
    friends = models.ManyToManyField('self', symmetrical=True, null=True, blank=True)
    home_location = models.ForeignKey(Location, related_name='home_location')
    current_location = models.ForeignKey(Location, related_name='current_location', blank=True, null=True)
    #achieved = models.ManyToOneRel(Achieved, related_name='achieved')

    def __unicode__(self):
        return self.last_name + ', ' + self.first_name

    def checkAchievments(self, new_only=True):

        point_totals = self.getPointTotals()
        met_score_requirements = self.checkScoreRequirements(point_totals)
        met_activity_requirements = self.checkActivityRequirements()
        met_requirements = met_activity_requirements + met_score_requirements

        newly_acheived = []

        #Now look at the acheivables to see what they got!
        for achievable in Achievable.objects.all():
            for requirement in achievable.requirements.all():
                if requirement in met_requirements:
                    newly_acheived.append(achievable)

        #Now remove anything that they already got
        if new_only:
            achieveds = Achieved.objects.all()
            for achieved in achieveds:
                if achieved in newly_acheived:
                    newly_acheived.remove(achieved)

            for achievable in newly_acheived:

                achieved = Achieved.objects.create()
                achieved.achievables.add(achievable)
                achieved.citizens.add(self)
                achieved.save()
                achievable.save()
                self.save()

        return newly_acheived



    def checkScoreRequirements(self, point_totals):
        score_reqs = ScoreRequirement.objects.all()
        met_score_requirements = []
        for score_req in score_reqs:
            for point_total in point_totals:
                if not point_total[0] == str(score_req.civic_type.name):
                    continue

                if point_total[1] >= score_req.reqPoints:
                    met_score_requirements.append(score_req)

        return met_score_requirements


    def checkActivityRequirements(self):
        records = ActivityRecord.objects.filter(citizen=self)
        met_activity_requirements = []
        activity_counts = {}

        for activity_req in ActivityRequirement.objects.all():
            for record in records:
                activity = record.activity
                if activity_req.activity == record.activity:

                    if activity in activity_counts:
                        activity_counts[activity] +=1
                    else:
                        activity_counts[activity] = 1

                    if activity_counts[activity] >= activity_req.reqCount:
                        met_activity_requirements.append(activity_req)

        return met_activity_requirements





    def getPointTotals(self):
        records = ActivityRecord.objects.filter(citizen=self)

        totals = {}

        for record in records:
            if not record.status == ActivityRecord.COMPLETED:
                continue

            civic_type = record.civic_type
            activity = record.activity
            points = activity.points

            if civic_type in totals:
                totals[civic_type] += points
            else:
                totals[civic_type] = points

        point_totals = []
        for key in totals.keys():
            point_totals.append( (str(key), totals[key]) )

        return point_totals

    def getPlannedEvents(self):
        records = ActivityRecord.objects.filter(citizen=self, status=ActivityRecord.PLANNED)

        plannedEvents = []

        for record in records:
            plannedEvents.append(record.activity)

        return plannedEvents


    def getFriendsPlannedEvents(self):

        plannedEvents = []

        for friend in self.friends.all():

            plannedEvents.append( (friend, friend.getPlannedEvents()) )

        return plannedEvents



class Organization(CivicProfile, Location):
    full_name = models.CharField(max_length=50)
    civic_type = models.ForeignKey(CivicType)
    url = models.URLField()
    organizer = models.ManyToManyField('self', symmetrical=True, null=False, blank=False)
    location = models.ForeignKey(Location, related_name='organization_location')

    def __unicode__(self):
        return self.full_name


class Activity(models.Model):
    name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='uploads')
    description = models.CharField(max_length=500)
    civic_type = models.ForeignKey(CivicType)
    location = models.ForeignKey(Location, related_name='location', blank=True, null=True)
    points = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name


class Event(Activity):
    cost = CurrencyField(decimal_places=2, max_digits=10, blank=True, default=0.00)
    start_date = models.DateField(default=datetime.now().date())
    start_time = models.TimeField(default=datetime.now().time())
    end_date = models.DateField(blank=True, default=None, null=True)
    end_time = models.TimeField(blank=True, default=None, null=True)


class AchievableRequirement(models.Model):
    """
    Tag requirement of an achievable.
    """
    pass

    def __unicode__(self):
        return ''


class ScoreRequirement(AchievableRequirement):
    """
    Requirement for minimum total score in a given type.
    """
    civic_type = models.ForeignKey(CivicType)
    reqPoints = models.PositiveIntegerField()

    def __unicode__(self):
        return unicode(self.reqPoints) + ' or more ' + unicode(self.civic_type)

class ActivityRequirement(AchievableRequirement):
    """
    Requirement for number of times a given activity must be completed.
    """
    activity = models.ForeignKey(Activity)
    reqCount = models.PositiveIntegerField()

    def __unicode__(self):
        return unicode(self.reqCount) + ' or more ' + unicode(self.activity)

class Achievable(models.Model):
    """This defines how to earn an achievement.
    """
    name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='uploads')
    description = models.CharField(max_length=50)
    requirements = models.ManyToManyField(AchievableRequirement, related_name='requirements')

    def __unicode__(self):
        return self.name

class Achieved(models.Model):
    """This is the achievement roll up for a user."""
    achievables = models.ManyToManyField(Achievable, related_name='achievables')
    citizens = models.ManyToManyField(Citizen, related_name='citizens')


class ActivityRecord(models.Model):

    RECORD_STATUS = (
        (u'Completed', u'Completed'),
        (u'Planned', u'Planned'),
        (u'Missed', u'Missed'),
    )

    COMPLETED = RECORD_STATUS[0][0]
    PLANNED = RECORD_STATUS[1][0]
    MISSED = RECORD_STATUS[2][0]

    activity = models.ForeignKey(Activity)
    citizen = models.ForeignKey(Citizen)
    civic_type = models.ForeignKey(CivicType)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=15, choices=RECORD_STATUS)


class Reward(models.Model):
    pass





