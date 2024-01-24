import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from django.conf import settings

class CustomUser(AbstractUser):
    pass

time_units_cust = tuple([(x, x[0].upper() + x[1:]) for x in settings.TIME_UNITS])

class CacheJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    url = models.TextField()
    time_int = models.IntegerField()
    time_frame = models.CharField(max_length=10, choices=time_units_cust)

class CacheItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(CacheJob, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    data = models.JSONField()
