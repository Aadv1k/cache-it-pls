from .models import CustomUser, CacheJob, CacheItem
from .services.job_runner import JobRunner

import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

job_runner = JobRunner()

def index(request):
    return render(request, "core/index.html")

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect(reverse("index"))

    user = CustomUser.objects.get(id=request.user.id)
    jobs = CacheJob.objects.filter(author=user)
    return render(request, "core/dashboard.html", {
        "jobs": jobs
    })

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse("index"))
        
@login_required
def api_ep_job(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid method'}, status=405) 

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    url = data.get("url")
    time_int = data.get("time_int")
    time_frame = data.get("time_frame")

    if not all((time_int, time_frame, url)):
        return JsonResponse({'error': "Bad input"}, status=400)

    try:
        res = requests.get(url)
        res.raise_for_status() 
    except requests.RequestException as e:
        return JsonResponse({'error': f'Request to {url} failed: {e}. Check to provide a different, valid URL'}, status=400)

    if  "application/json" not in res.headers["Content-Type"].lower():
        return JsonResponse({'error': f'Expected JSON response for {url}, found <code>{res.headers["Content-Type"]}</code>'}, status=415) 

    if CacheJob.objects.filter(url=url).exists():
        return JsonResponse({'error': 'The URL already exists, and is being cached. You should edit it instead'}, status=400)

    cache_job = CacheJob.objects.create(author=request.user, url=url, time_int=time_int, time_frame=time_frame)

    job_runner.execute_job(cache_job)
    job_runner.schedule_job(cache_job)

    return JsonResponse({'message': 'Job created successfully', 'job_id': cache_job.id})

def api_single_ep_job(request, id):
    try:
        api_instance = CacheJob.objects.get(id=id)
    except CacheJob.DoesNotExist:
        return JsonResponse({'error': 'API not found.'}, status=404)

    if request.method == "DELETE":
        api_instance.delete()
        return JsonResponse({'message': 'API successfully deleted.'})
    elif request.method == "GET":
        latest_cache = CacheItem.objects.filter(owner=api_instance).order_by("timestamp").first()
        print(latest_cache)
        return JsonResponse(latest_cache.data, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
