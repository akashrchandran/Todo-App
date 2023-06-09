import datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Todo


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
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]

    # Ensure password matches confirmation
    password = request.POST["password"]

    # Attempt to create new user
    try:
        user = User.objects.create_user(username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
    except IntegrityError:
        return render(request, "signup.html", {
            "messages": ["Username already taken."]
        })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))

@login_required
def index(request):
    if request.method == 'POST':
        task = request.POST['task']
        date = request.POST['date']
        print(date)
        todo = Todo.objects.create(username=request.user.username, task=task, date=date)
        todo.save()
        return redirect(reverse(index))
    completed = Todo.objects.filter(username=request.user.username, completed=True)
    todos = Todo.objects.filter(username=request.user.username, completed=False, date__gte=datetime.date.today())
    expired = Todo.objects.filter(username=request.user.username, completed=False, date__lt=datetime.date.today())
    return render(request, 'index.html', {'todos': todos, 'completed': completed, 'expired': expired, 'first_name': request.user.first_name, 'last_name': request.user.last_name})

@login_required
@csrf_exempt
def delete_todo(request, identifier):
    if request.method == 'POST':
        try:
            todo = Todo.objects.get(id=identifier, username=request.user.username)
            todo.delete()
            return JsonResponse({'status': 200, 'msg': "Todo deleted"}, status=200)
        except Todo.DoesNotExist:
            return JsonResponse({'status': 404, 'msg': "The todo doesn't seem to exist"}, status=404)
    else:
        redirect(reverse(index))
        
@login_required
@csrf_exempt
def update_todo(request, identifier):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            todo = Todo.objects.get(id=identifier, username=request.user.username)
            todo.task = body['updatedTask']
            todo.date = body['updatedDate']
            todo.save()
            return JsonResponse({'status': 200, 'msg': "Todo updated"}, status=200)
        except Todo.DoesNotExist:
            return JsonResponse({'status': 404, 'msg': "The todo doesn't seem to exist"}, status=404)
    else:
        redirect(reverse(index))

@login_required
@csrf_exempt
def toggle_complete_todo(request, identifier):
    if request.method == 'POST':
        try:
            todo = Todo.objects.get(id=identifier, username=request.user.username)
            todo.completed = not todo.completed
            todo.save()
            return JsonResponse({'status': 200, 'msg': "Todo completed"}, status=200)
        except Todo.DoesNotExist:
            return JsonResponse({'status': 404, 'msg': "The todo doesn't seem to exist"}, status=404)
    else:
        redirect(reverse(index))
