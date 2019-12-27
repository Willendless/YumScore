from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_name = models.CharField('姓名', max_length=100)
    user_identifier = models.CharField(max_length=22, blank=True, default='null', unique=True)
    user_review_count = models.IntegerField(default=0)
    user_date = models.DateTimeField(default=timezone.now)
    user_average_stars = models.FloatField(default=0)
    user_fans = models.IntegerField(default=0)
    user_useful_votes = models.IntegerField(default=0)
    user_funny_votes = models.IntegerField(default=0)
    user_cool_votes = models.IntegerField(default=0)
    #user_friends = models.ManyToManyField('self', default='null', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["-user_date"]
        verbose_name = "用户"
        verbose_name_plural = "用户"
