from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.utils.timezone import now, localtime
import random
import json


def login_view(request):
    if request.method != "POST":
        return (
            HttpResponseRedirect(reverse("index"))
            if request.user.is_authenticated
            else render(request, "signin.html")
        )
    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        messages.error(request, "Invalid username and/or password.")
        return redirect(reverse(login_view))

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method != "POST":
        return render(request, "signup.html")
    username = request.POST["username"]
    email = request.POST["email"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]

    # Ensure password matches confirmation
    password = request.POST["password"]

    # Attempt to create new user
    try:
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
    except IntegrityError:
        return render(request, "signup.html", {
            "message": "Username already taken."
        })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))

@login_required
def index(request):
    return HttpResponse("Hello, world. You're at the signup_signin index.")