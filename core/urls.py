from django.urls import path

from .views import *

urlpatterns = [
    path("", view=index, name="index"),

    path("dashboard/", view=dashboard, name="dashboard"),
    path("logout/", view=logout_user, name="logout_user"),
]
