from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

import requests

from django.conf import settings

from .models import CustomUser, CacheJob

def index(request):
    return render(request, "core/index.html")

@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse("index"))
        

def oauth_google(request):
    google_auth_url = "".join([
        f"{settings.GOOGLE_OAUTH_AUTH_URI}?",
        f"client_id={settings.GOOGLE_OAUTH_CLIENT_ID}",
        f"&redirect_uri={settings.GOOGLE_OAUTH_CALLBACK_URL}",
        "&response_type=code",
        "&scope=email profile"
    ])

    return redirect(google_auth_url)

def oauth_google_callback(request):
    if request.method != "GET":
        return HttpResponse("Method not allowed", status=405)

    code = request.GET.get('code')

    if not code:
        return HttpResponse("Bad input", status=400)

    google_token_params = {
        "code": code,
        "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
        "grant_type": "authorization_code"
    }

    auth_res = requests.post(settings.GOOGLE_OAUTH_TOKEN_URI, data=google_token_params)

    if not auth_res.ok:
        return HttpResponse("Failed to obtain authorization token from Google", status=500)

    auth_data = auth_res.json()
    auth_token = auth_data.get("access_token")

    if not auth_token:
        return HttpResponse("Failed to obtain access token from Google", status=500)

    user_res = requests.get(settings.GOOGLE_OAUTH_USER_PROFILE, headers={"Authorization": f"Bearer {auth_token}"})

    if not user_res.ok:
        return HttpResponse("Failed to obtain user profile from Google", status=500)

    user_data = user_res.json()
    user_email = user_data.get("email")
    user_username = user_data.get("given_name")

    try:
        found_user = CustomUser.objects.get(email=user_email)
        login(request, found_user)
    except CustomUser.DoesNotExist:
        new_user = CustomUser.objects.create(email=user_email, username=user_username)
        login(request, new_user)

    return HttpResponseRedirect(reverse("dashboard"))

@login_required
def api_job(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid method'}, status=405) 

    url = request.POST.get("url", "")
    time_int = request.POST.get("time_int", "")
    time_frame = request.POST.get("time_frame", "")


    try:
        res = requests.get(url)
        res.raise_for_status() 
    except requests.RequestException as e:
        return JsonResponse({'error': f'Request to {url} failed: {e}'}, status=500)

    if res.headers["Content-Type"] != "application/json":
        return JsonResponse({'error': 'Invalid Content-Type'}, status=415) 

    cache_job = CacheJob.objects.create(url=url, time_int=time_int, time_frame=time_frame)

    return JsonResponse({'message': 'Job created successfully', 'job_id': cache_job.id})
