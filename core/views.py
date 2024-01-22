from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login

import requests

from django.conf import settings

from .models import User

def index(request):
    return render(request, "core/index.html")

def oauth_google(request):
    google_auth_url = "".join([
        f"{settings.GOOGLE_OAUTH_AUTH_URI}?",
        f"client_id={settings.GOOGLE_OAUTH_CLIENT_ID}",
        f"&redirect_uri={settings.GOOGLE_OAUTH_CALLBACK_URL}",
        "&response_type=code",
        "&scope=email profile"
    ])

    return redirect(google_auth_url)

import requests
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings

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
        found_user = User.objects.get(email=user_email)
        login(request, found_user)
        return HttpResponse(f"Welcome back! {found_user.username}")
    except User.DoesNotExist:
        new_user = User.objects.create(email=user_email, username=user_username)
        login(request, new_user)
        return HttpResponse("Successfully obtained user credentials", status=200)
