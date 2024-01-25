from .models import CustomUser, CacheJob, CacheItem

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

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
