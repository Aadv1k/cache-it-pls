from django.db import models
import uuid
from datetime import timedelta

class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)

class CacheItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(CacheJob, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    data = models.TextField()

class CacheJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    url = models.TextField()
    time_quantity = models.IntegerField()
    
    TIME_UNITS = (
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
    )
    time_unit = models.CharField(max_length=10, choices=TIME_UNITS)
    
    def to_cron_str(self) -> str:
        if self.time_unit == 'minutes':
            return f'*/{self.time_quantity} * * * *'
        elif self.time_unit == 'hours':
            return f'0 */{self.time_quantity} * * *'
        elif self.time_unit == 'days':
            return f'0 0 */{self.time_quantity} * *'

        return None
