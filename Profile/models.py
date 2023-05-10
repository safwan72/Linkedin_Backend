from django.db import models
from django.forms import CharField
from auth_api.models import UserProfile

# Create your models here.


class ContactInfo(models.Model):
    website = models.URLField(
        blank=True,
        max_length=255,
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="contactme"
    )

    class Meta:
        verbose_name_plural = "User Contact Info"
        db_table = "User Contact Info"

    def __str__(self):
        return self.user.user.email + " 's Contact Info"


class Headline(models.Model):
    header = models.CharField(blank=True, max_length=255)
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="myheader"
    )

    class Meta:
        verbose_name_plural = "User Headline"
        db_table = "User Headline"

    def __str__(self):
        return self.user.user.email + " 's Headline"


class AboutSection(models.Model):
    description = models.TextField(blank=True)
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="myabout"
    )

    class Meta:
        verbose_name_plural = "User About"
        db_table = "User About"

    def __str__(self):
        return self.user.user.email + " 's About"


def upload_featured(instance, filename):
    return "featured/{instance.user.user.email}/{instance.user.user.username}_featured.png".format(
        instance=instance
    )


class FeaturedSection(models.Model):
    description = models.TextField(blank=True)
    title = models.CharField(blank=True, max_length=255)
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="myfeatured"
    )
    picture = models.ImageField(upload_to=upload_featured, blank=True, null=True)
    link = models.URLField(
        blank=True,
        max_length=255,
    )

    class Meta:
        verbose_name_plural = "User Featured"
        db_table = "User Featured"

    def __str__(self):
        return self.user.user.email + " 's Featured"


class WorkExperience(models.Model):
    TYPE = (
        ("Fulltime", "Full-Time"),
        ("Parttime", "Part-Time"),
        ("Internship", "Internship"),
        ("Contract", "Contract"),
        ("Apprenticeship", "Apprenticeship"),
        ("Seasonal", "Seasonal"),
        ("Selfemployed", "Self-employed"),
        ("Freelance", "Freelance"),
    )
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="workexperience"
    )
    title = models.CharField(max_length=255)
    employment_type = models.CharField(choices=TYPE, max_length=50)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    currently_working = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User Work Experience"
        db_table = "User Work Experience"
        ordering = ("-start_date",)

    def __str__(self):
        return (
            self.user.user.email
            + " 's workexperience "
            + self.company
            + " "
            + self.title
        )


class Education(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="myeducation"
    )
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, blank=True, null=True)
    field_of_study = models.CharField(max_length=255, blank=True, null=True)
    grade = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    currently_studying = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    activities = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "User Education"
        db_table = "User Education"

    def __str__(self):
        return self.user.user.email + " 's educations"


class SkillList(models.Model):
    skill = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Skill List"
        db_table = "Skill List"

    def __str__(self):
        return self.skill


class Skills(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="myskills"
    )
    skill = models.ForeignKey(
        SkillList, on_delete=models.CASCADE, related_name="skillList"
    )
    top_skill = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User Skills"
        db_table = "User Skills"

    def __str__(self):
        return self.user.user.username + " skills"
