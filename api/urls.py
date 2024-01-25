from django.urls import path
from .views import *

urlpatterns = [
    path("job/", view=handle_create_job, name="api/job"),
    path("job/<str:id>", view=handle_job_by_id, name="api/job/id")
]
