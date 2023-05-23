from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", default="default/user.png", blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    post_content = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(default=now)
    image = models.ImageField(upload_to="images", default="", blank=True)

    def __str__(self):
        return f"Post {self.pk}"


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    reply_content = models.CharField(max_length=5000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)
    image = models.ImageField(upload_to="images", default="", blank=True)

    def __str__(self):
        return f"Reply {self.pk} for Post {self.post.pk}"
