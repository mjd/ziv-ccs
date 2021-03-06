from django.contrib.auth.models import User

__author__ = 'jlparise'

from django.forms import ModelForm
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


from models import Citizen, Location


class LocationForm(ModelForm):
    class Meta:
        model = Location


class CitizenForm(ModelForm):

    """A form for creating new users. Includes all the
       required fields, plus a repeated password.
    """
    username = forms.CharField()
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput)



    class Meta:
        model = Citizen
        fields = ('first_name', 'last_name', 'email', 'avatar')
        exclude = ('user', 'current_location', 'friends', 'home_location')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError(msg)
        return password2

    def save(self, commit=True):

        #citizen Data
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password1")
        email = self.cleaned_data.get('email')
        avatar = self.cleaned_data.get('avatar')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        # Save the provided password in hashed format
        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)

        if commit:
           user.save()


        return user


"""
user = models.ForeignKey(User, unique=True)
    avatar = models.ImageField(upload_to='uploads')


class Citizen(CivicProfile):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 50)
    friends = models.ManyToManyField('self', symmetrical=True, null=True, blank=True)
    home_location = models.ForeignKey(Location, related_name='home_location')
    current_location = models.ForeignKey(Location, related_name='current_location', blank=True, null=True)
"""


