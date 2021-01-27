from django.contrib.auth.models import User
from django.db import models
from datetime import timezone


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    profile_img = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    media = models.FileField(upload_to='user_files/', blank=True)
    likes = models.ManyToManyField(Profile, related_name='likes', blank=True)
    retweets = models.ManyToManyField(Profile, related_name='retweets', blank=True)

    def __str__(self):
        return self.content

    # def __eq__(self, other):
    #     # return self.profile.user.username == other.profile.user.username and self.content == other.content
    #     return self.id == other.id

    class Meta:
        ordering = ('-pub_date',)


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.profile.user.username

    class Meta:
        ordering = ('-pub_date',)

# class Likes(models.Model):
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
#     post = models.ManyToManyField(Post)
#
#     def __str__(self):
#         return self.profile.user.username
