from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from . import models
admin.site.register(models.UserProfile)
