__author__ = 'jlparise'


from django.contrib import admin

import models


class UserAdmin(admin.ModelAdmin):

    model = models.User

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Profile)
admin.site.register(models.Organization)
admin.site.register(models.Organizer)
admin.site.register(models.Achievable)
admin.site.register(models.Achieved)
admin.site.register(models.Activity)
admin.site.register(models.Event)
admin.site.register(models.Reward)