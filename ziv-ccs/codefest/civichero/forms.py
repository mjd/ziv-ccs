__author__ = 'jlparise'

from django.forms import ModelForm


from models import Citizen


class CitizenForm(ModelForm):
    class Meta:
        model = Citizen