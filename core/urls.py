from django.urls import path

from .views import *

urlpatterns = [
    path("", view=index, name="index"),

    path("oauth/google/", view=oauth_google, name="oauth_google"),
    path("oauth/google/callback", view=oauth_google_callback, name="oauth_google_callback"),


    path("dashboard/", view=dashboard, name="dashboard"),
    path("logout/", view=logout_user, name="logout_user"),

    path("api/job", view=api_ep_job, name="api/job"),
    path("api/job/<str:id>", view=api_single_ep_job, name="api/job/id")
]
