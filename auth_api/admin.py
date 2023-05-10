from django.contrib import admin
from . import models
from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    exclude = ["id"]


admin.site.register(models.User, UserAdmin)
# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileView)
admin.site.register(models.Followers)
admin.site.unregister(Group)
