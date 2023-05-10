import random
from django.db import models
from auth_api.models import UserProfile
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models import signals
import os


def photo_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    randomstr = "".join((random.choice(chars)) for x in range(10))
    return "post/{useremail}/{basename}{randomstring}{ext}".format(
        useremail=instance.author.user.email,
        basename=basefilename,
        randomstring=randomstr,
        ext=file_extension,
    )


class Post(models.Model):
    author = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="post_author"
    )
    post_image = models.ImageField(upload_to=photo_path, blank=True, null=True)
    post_title = models.TextField(max_length=264)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=264, unique=True, blank=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "User POST"
        db_table = "User POST"
        ordering = ("-upload_date",)

    def __str__(self):
        return self.author.user.email + " 's Post"


@receiver(signals.pre_save, sender=Post)
def populate_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.post_title)


class Like(models.Model):
    liker = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="post_liker"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_like_post"
    )
    date = models.DateTimeField(auto_now_add=True)
    liked = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User POST Liked"
        db_table = "User POST Liked"
        unique_together = (
            "post",
            "liker",
        )

    def __str__(self):
        return self.liker.user.email + " Liked " + self.post.post_title + " "


@receiver(signals.post_save, sender=Like)
def save_like(sender, instance, created, **kwargs):
    if created:
        instance.liked = True
        instance.save()


class Comment(models.Model):
    commenter = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="post_commenter"
    )
    comment_text = models.TextField(max_length=264)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comment_post"
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "User POST Comment"
        db_table = "User POST Comment"

    def __str__(self):
        return self.commenter.user.email + " Commented On " + self.post.post_title + " "
