from django.urls import path
from .views import *

urlpatterns = [
    path("google/", view=oauth_google, name="oauth_google"),
    path("google/callback", view=oauth_google_callback, name="oauth_google_callback"),
]
