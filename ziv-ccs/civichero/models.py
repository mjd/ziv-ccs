from django.db import models

# Create your models here.


class CivicType(models.Model):
    avatar = models.ImageField(upload_to='uploads')
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name


class Profile(models.Model):

    screen_name = models.CharField(max_length = 25)
    avatar = models.ImageField(upload_to='uploads')



class User(Profile):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 50)
    friends = models.ManyToManyField('self', symmetrical=True, null=True, blank=True)

    def __unicode__(self):
        return self.last_name + ', ' + self.first_name


class Organization(Profile):
    full_name = models.CharField(max_length = 50)
    civicType = models.ManyToOneRel(CivicType,"civicType")
    url = models.URLField()
    organizer = models.ManyToManyField('self', symmetrical=True, null=False, blank=False)

    def __unicode__(self):
        return self.full_name


class Achievable(models.Model):
    """This defines how to earn an achievement.
    TODO define requirements
    """
    avatar = models.ImageField(upload_to='uploads')
    description = models.CharField(max_length = 50)



class Achieved(models.Model):
    """This is the achievement roll up for a user."""
    pass


class Activity(models.Model):
    avatar = models.ImageField(upload_to='uploads')
    description = models.CharField(max_length = 50)
    civicType = models.ManyToOneRel(CivicType,"civicType")
    points = models.PositiveIntegerField()


class Event(Activity):
    pass


class Reward(models.Model):
    pass





