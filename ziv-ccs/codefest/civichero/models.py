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


class Organization(CivicProfile, Location):
    full_name = models.CharField(max_length=50)
    civic_type = models.ForeignKey(CivicType)
    url = models.URLField()
    organizer = models.ManyToManyField('self', symmetrical=True, null=False, blank=False)
    location = models.ForeignKey(Location, related_name='organization_location')

    def __unicode__(self):
        return self.full_name


class Achievable(models.Model):
    """This defines how to earn an achievement.
    TODO define requirements
    """
    name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='uploads')
    description = models.CharField(max_length=50)


class Achieved(models.Model):
    """This is the achievement roll up for a user."""
    achievables = models.ManyToManyField(Achievable, related_name='achievables')
    citizens = models.ManyToManyField(Citizen, related_name='citizens')


class Activity(models.Model):
    name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='uploads')
    description = models.CharField(max_length=500)
    civic_type = models.ForeignKey(CivicType)
    location = models.ForeignKey(Location, related_name='activity_location', blank=True, null=True)
    points = models.PositiveIntegerField()


class Event(Activity):
    event_location = models.ForeignKey(Location, related_name='event_location')
    cost = CurrencyField(decimal_places=2, max_digits=10, blank=True, default=0.00)
    start_date = models.DateField(default=datetime.now().date())
    start_time = models.TimeField(default=datetime.now().time())
    end_date = models.DateField(blank=True, default=None, null=True)
    end_time = models.TimeField(blank=True, default=None, null=True)


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





