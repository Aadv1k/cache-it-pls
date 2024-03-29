from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include("oauth.urls")),
    path('api/', include("api.urls")),
    path("", include("core.urls"))
]
