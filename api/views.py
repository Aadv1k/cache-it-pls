from core.services.job_runner import JobRunner
from core.models import CacheJob, CacheItem

import json

from django.http import JsonResponse

job_runner = JobRunner()

def handle_create_job(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401) 

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

def handle_job_by_id(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401) 
    try:
        api_instance = CacheJob.objects.get(id=id)
    except CacheJob.DoesNotExist:
        return JsonResponse({'error': 'API not found.'}, status=404)

    if request.method == "DELETE":
        api_instance.delete()
        return JsonResponse({'message': 'API successfully deleted.'})
    elif request.method == "GET":
        latest_cache = CacheItem.objects.filter(owner=api_instance).order_by("timestamp").first()
        return JsonResponse(latest_cache.data, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
