from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import TeacherRegistrationForm, TeacherLoginForm
from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponse("Hello, this is the index view.")

def homepage(request):
    return HttpResponse("Hello! This is the homepage at the root URL.")

def index(request):
    return HttpResponse("Hello, this is the index view.")

def homepage(request):
    return HttpResponse("Hello! This is the homepage at the root URL.")

def register_teacher(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")  # Redirect to teacher dashboard
    else:
        form = TeacherRegistrationForm()
    return render(request, "auth/register.html", {"form": form})

def login_teacher(request):
    if request.method == "POST":
        form = TeacherLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = TeacherLoginForm()
    return render(request, "auth/login.html", {"form": form})

@login_required
def logout_teacher(request):
    logout(request)
    return redirect("login_teacher")  # Redirect to login page after logout

