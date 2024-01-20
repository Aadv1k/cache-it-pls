from django.contrib import admin

from .models import User, CacheJob, CacheItem

admin.site.register(User)
admin.site.register(CacheJob)
admin.site.register(CacheItem)
