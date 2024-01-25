from django.urls import path
from .views import *

urlpatterns = [
    path("job", view=handle_job, name="api_job"),
    path("job/<str:id>", view=handle_job_by_id, name="api_job_id")
]
