from django.db import models

# Create your models here.


class Profile(models.Model):

    screen_name = models.CharField(max_length = 25)
    email = models.EmailField(max_length = 50)
    avatar = models.ImageField(upload_to='uploads')



class User(Profile):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    friends = models.ManyToManyField('self', symmetrical=True, null=True, blank=True)

    def __unicode__(self):
        return self.last_name + ', ' + self.first_name

class Organization(Profile):
    pass


class Organizer(models.Model):
    pass


class Achievable(models.Model):
    """This defines how to earn an achievement.
    """
    pass


class Achieved(models.Model):
    """This is the achievement roll up for a user."""
    pass


class Activity(models.Model):
    pass


class Event(Activity):
    pass


class Reward(models.Model):
    pass




