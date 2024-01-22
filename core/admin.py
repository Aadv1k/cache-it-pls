from django.contrib import admin

from .models import CustomUser, CacheJob, CacheItem

admin.site.register(CustomUser)
admin.site.register(CacheJob)
admin.site.register(CacheItem)
