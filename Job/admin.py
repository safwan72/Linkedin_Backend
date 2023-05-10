from django.contrib import admin
from . import models

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    exclude = ["id"]


admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.CompanyAboutSection)
admin.site.register(models.CompanyFollowers)
admin.site.register(models.CompanyPost)
admin.site.register(models.CompanyPostLike)
admin.site.register(models.CompanyPostComment)
admin.site.register(models.CompanyJobs)
admin.site.register(models.SavedJobs)
