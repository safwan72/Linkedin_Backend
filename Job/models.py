from typing import Type
from django.db import models
from auth_api.models import UserProfile
import os
import random
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models import signals
from django_random_id_model import RandomIDModel

# Create your models here.
def photo_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    randomstr = "".join((random.choice(chars)) for x in range(10))
    return "company/logo/{user}/{randomstring}{ext}".format(
        user=instance.created_by.user.username,
        randomstring=randomstr,
        ext=file_extension,
    )


def cover_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    randomstr = "".join((random.choice(chars)) for x in range(10))
    return "company/cover_photo/{user}/{randomstring}{ext}".format(
        user=instance.created_by.user.username,
        randomstring=randomstr,
        ext=file_extension,
    )


class Company(RandomIDModel):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="my_company"
    )
    logo = models.ImageField(upload_to=photo_path, blank=True, null=True)
    cover_photo = models.ImageField(upload_to=cover_path, blank=True, null=True)
    headline = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Company"
        db_table = "Company"

    def __str__(self):
        return self.name


SIZE = (
    ("10", "1-10"),
    ("50", "10-50"),
    ("100", "50-100"),
    ("500", "100-500"),
    ("1000", "500-1000"),
    ("5000", "1000-5000"),
    ("10000", "5000-10000"),
    ("10000", "10000+"),
)
TYPE = (
    ("Public", "Public"),
    ("Government", "Government"),
    ("Private", "Private"),
    ("Nonprofit", "Nonprofit"),
)


class CompanyAboutSection(models.Model):
    description = models.TextField(blank=True)
    company = models.OneToOneField(
        Company, on_delete=models.CASCADE, related_name="mycompanyabout"
    )
    size = models.CharField(choices=SIZE, default=None, max_length=50, null=True)
    type = models.CharField(choices=TYPE, default=None, max_length=50, null=True)
    phone = models.CharField(max_length=20, blank=True)
    industry = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(
        blank=True,
        max_length=255,
    )
    founded = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Company About"
        db_table = "Company About"

    def __str__(self):
        return self.company.name + " 's About"


def post_path(instance, filename):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    randomstr = "".join((random.choice(chars)) for x in range(10))
    return "company/posts/{company}/{randomstring}.png".format(
        company=instance.company.name,
        randomstring=randomstr,
    )


class CompanyPost(models.Model):
    title = models.TextField(blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="mycompanypost"
    )
    photo = models.ImageField(upload_to=post_path, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Company Post"
        db_table = "Company Post"
        ordering = ("-upload_date",)

    def __str__(self):
        return self.company.name + " 's Post"


class CompanyJobs(models.Model):
    job_title = models.CharField(max_length=200, blank=True)
    job_description = models.TextField(blank=True)
    posted_by = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_job_post"
    )
    applied = models.ManyToManyField(
        UserProfile, related_name="company_job_appliers", blank=True
    )
    posted_at = models.DateTimeField(auto_now_add=True)
    isOpen = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "CompanyJobs"
        db_table = "CompanyJobs"
        ordering = ("-posted_at",)

    def __str__(self):
        return self.job_title + " by " + self.posted_by.name


class SavedJobs(models.Model):
    job = models.ForeignKey(
        CompanyJobs, on_delete=models.CASCADE, related_name="saved_company_jobs"
    )
    me = models.ForeignKey(
        UserProfile,
        related_name="company_job_savedby_Me",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "My Saved Jobs"
        db_table = "My Saved Jobs"
        unique_together = (
            "job",
            "me",
        )

    def __str__(self):
        return self.me.user.username + " Saved Jobs "


class CompanyFollowers(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="followers_of_myCompanny"
    )
    myfollowers = models.ManyToManyField(
        UserProfile, related_name="my_company_followers", blank=True
    )

    class Meta:
        verbose_name_plural = "Company Follower's"
        db_table = "Company Follower's"

    def __str__(self):
        return self.company.name + " 's Follower's"


@receiver(signals.post_save, sender=Company)
def create_company_profile(sender, instance, created, **kwargs):
    if created:
        CompanyFollowers.objects.create(company=instance)


class CompanyPostLike(models.Model):
    liker = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="company_post_liker"
    )
    post = models.ForeignKey(
        CompanyPost, on_delete=models.CASCADE, related_name="company_post_post_like"
    )
    date = models.DateTimeField(auto_now_add=True)
    liked = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "CompanyPost Like"
        db_table = "CompanyPost Like"
        unique_together = (
            "post",
            "liker",
        )

    def __str__(self):
        return self.liker.user.email + " Liked " + self.post.company.name + " 's Post"


@receiver(signals.post_save, sender=CompanyPostLike)
def save_like(sender, instance, created, **kwargs):
    if created:
        instance.liked = True
        instance.save()


class CompanyPostComment(models.Model):
    commenter = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="company_post_commenter"
    )
    comment_text = models.TextField(max_length=264)
    post = models.ForeignKey(
        CompanyPost, on_delete=models.CASCADE, related_name="company_post_comment_post"
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "CompanyPost Comment"
        db_table = "CompanyPost Comment"

    def __str__(self):
        return self.commenter.user.email + " Commented On " + self.post.title + " "
