from django.conf import settings
import requests
import schedule
from core.models import CacheItem

class JobRunner:
    jobs = {}

    def execute_job(self, cache_job):
        url = cache_job.url
        response = requests.get(url)
        data = response.json()
        CacheItem.objects.create(owner=cache_job, data=data)

    def schedule_job(self, cache_job):
        tf = cache_job.time_frame.lower()
        ti = int(cache_job.time_int)

        if tf not in settings.TIME_UNITS:
            return None

        job_id = None
        if tf == "minutes":
            job_id = schedule.every(ti).minutes.do(self.execute_job, job=cache_job)
        elif tf == "hours":
            job_id = schedule.every(ti).hours.do(self.execute_job, job=cache_job)
        elif tf == "days":
            job_id = schedule.every(ti).days.do(self.execute_job, job=cache_job)
        else:
            assert False, "This can't be reached, since this is internally called"

        self.jobs[cache_job.id] = job_id

    def deschedule_job(self, job_id):
        assert job_id in self.jobs

        schedule.cancel_job(self.jobs[job_id])
        del self.jobs[job_id]
