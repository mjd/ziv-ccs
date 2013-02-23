from django.db import models

# Create your models here.


class User(models.Model):

    login = models.CharField(max_length = 25)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
