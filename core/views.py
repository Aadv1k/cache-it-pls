from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login

import requests

from .const import *

def index(request):
    return render(request, "core/index.html")

def oauth_google(request):
    google_auth_url = "".join([
        f"{GOOGLE_OAUTH_AUTH_URI}?",
        f"client_id={GOOGLE_OAUTH_CLIENT_ID}",
        f"&redirect_uri={GOOGLE_OAUTH_CALLBACK_URL}",
        "&response_type=code",
        "&scope=email profile"
    ])

    return redirect(google_auth_url)

def oauth_google_callback(request):
    if request.method != "GET":
       return HttpResponse("Method not valid", status=405)

    code = request.GET.get('code')

    if not code or not len(code):
        return HttpResponse("Bad input", status=401)


    google_token_params = {
        "code": code,
        "client_id": GOOGLE_OAUTH_CLIENT_ID,
        "client_secret": GOOGLE_OAUTH_CLIENT_SECRET,
        "redirect_uri": GOOGLE_OAUTH_CALLBACK_URL,
        "grant_type": "authorization_code"
    }

    auth_res = requests.post(GOOGLE_OAUTH_TOKEN_URI, data=google_token_params)
    if not auth_res.ok:
        return HttpResponse("Internal error when obtaining authorization token from google", status=500)

    auth_data = auth_res.json()
    auth_token = auth_data.get("access_token")

    user_res = requests.get(GOOGLE_OAUTH_USER_PROFILE, headers={ "Authorization": f"Bearer {auth_token}" })
    user_data = user_res.json()

    found_user = User.objects.get(email=user_data.email)

    if found_user is not None:
        login(request, found_user)
        return HttpResponse(f"Welcome back! {found_user.username}")

    # TODO: change password logic to a random generator 
    new_user = User.objects.create(email=user_data.email, username=found_user.given_name)

    login(request,  new_user)


    return HttpResponse("Successfully obtained user credentials", status=200)
