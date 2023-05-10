from django.db import models

# To Create A Custom User Model and admin panel
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import randint
from django_random_id_model import RandomIDModel

# Create your models here.


def generate_random_id():
    return randint(10 ** (5 - 1), (10**5) - 1)


class MyuserManager(
    BaseUserManager
):  # To Manage new users using this baseusermanaegr class
    """A Custom User Manager to deal with Emails  as an unique Identifier"""

    def create_user(self, email, username, password, **extra_fields):
        """Creates and Saves an user with given email and password"""

        if not email:
            raise ValueError("Email Must Be Set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("SuperUser is_staff must be True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("SuperUser is_superuser must be True")

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, RandomIDModel):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=264, null=False)
    is_staff = models.BooleanField(
        gettext_lazy("staff_status"),
        default=False,
        help_text="Determines Whether They Can Log in this Site or not",
    )
    is_active = models.BooleanField(
        gettext_lazy("active"),
        default=True,
        help_text="Determines Whether their Account Status is Active or not",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]
    objects = MyuserManager()

    class Meta:
        verbose_name_plural = "User"
        db_table = "User"

    def __str__(self):
        return self.email + " <> " + self.username


def upload_image(instance, filename):
    return "profile/{instance.user.email}/{instance.user.email}profile_pic.png".format(
        instance=instance
    )


def upload_cover(instance, filename):
    return "profile/{instance.user.email}/{instance.user.email}cover_pic.png".format(
        instance=instance
    )


class UserProfile(models.Model):
    first_name = models.CharField(max_length=264, blank=True)
    last_name = models.CharField(max_length=264, blank=True)
    profile_pic = models.ImageField(
        upload_to=upload_image, blank=True, default="/profile/default.jpg"
    )
    cover_pic = models.ImageField(
        upload_to=upload_cover, blank=True, default="/profile/defaultCover.png"
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="userprofile",
    )

    class Meta:
        verbose_name_plural = "User Profile"
        db_table = "User Profile"

    def __str__(self):
        return self.user.email + " 's Profile"


class ProfileView(models.Model):
    myProfile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="my_profile_view"
    )
    viewer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="my_profile_viewer"
    )

    class Meta:
        verbose_name_plural = "User Profile Views"
        db_table = "User Profile Views"

    def __str__(self):
        return (
            self.viewer.user.email
            + " Viewed "
            + self.myProfile.user.email
            + " 's Profile"
        )


class Followers(models.Model):
    me = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="followers_of_me"
    )
    myfollowers = models.ManyToManyField(
        UserProfile, related_name="my_followers", blank=True
    )

    class Meta:
        verbose_name_plural = "User Follower's"
        db_table = "User Follower's"

    def __str__(self):
        return self.me.user.email + " 's Follower's"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Followers.objects.create(me=instance.userprofile)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.userprofile.save()
