from django.contrib.auth.models import User
from django.db import models
from datetime import timezone


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    profile_img = models.ImageField(upload_to='avatars', blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    media = models.FileField(upload_to='media', blank=True)
    is_liked = False

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('-pub_date', )


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.profile.user.username

    class Meta:
        ordering = ('-pub_date', )


class Likes(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username
