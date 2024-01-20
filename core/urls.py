from django.urls import path

from .views import *

urlpatterns = [
    path("", view=index, name="index"),

    path("oauth/google/", view=oauth_google, name="oauth_google"),
    path("oauth/google/callback", view=oauth_google_callback, name="oauth_google_callback"),
]
