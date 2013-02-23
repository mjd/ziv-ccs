__author__ = 'jlparise'


from django.contrib import admin

import models


class UserAdmin(admin.ModelAdmin):

    model = models.User

admin.site.register(models.User, UserAdmin)