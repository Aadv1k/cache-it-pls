from django.urls import path

from .views import *

urlpatterns = [
    path("", view=index, name="index"),

    path("oauth/google/", view=oauth_google, name="oauth_google"),
    path("oauth/google/callback", view=oauth_google_callback, name="oauth_google_callback"),


    path("dashboard/", view=dashboard, name="dashboard"),
    path("logout/", view=logout, name="logout_user"),

    path("/api/job", view=api_job, name="api_job")

]
