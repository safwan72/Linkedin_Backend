from django.contrib import admin
from . import models

# Register your models here.


class ChatInline(admin.TabularInline):
    model = models.Chat


class ThreadAdmin(admin.ModelAdmin):
    inlines = [
        ChatInline,
    ]


admin.site.register(models.Thread, ThreadAdmin)
admin.site.register(models.Chat)
