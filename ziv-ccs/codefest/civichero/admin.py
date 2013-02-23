__author__ = 'jlparise'


from django.contrib import admin

import models


class UserAdmin(admin.ModelAdmin):

    model = models.Citizen

admin.site.register(models.Citizen, UserAdmin)
admin.site.register(models.CivicProfile)
admin.site.register(models.Organization)
admin.site.register(models.Achievable)
admin.site.register(models.Achieved)
admin.site.register(models.Activity)
admin.site.register(models.Event)
admin.site.register(models.Reward)
admin.site.register(models.Location)
