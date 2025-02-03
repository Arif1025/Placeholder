from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import CustomLoginForm
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Hello, this is the index view.")

def homepage(request):
    return HttpResponse("Hello! This is the homepage at the root URL.")

def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            role = form.cleaned_data.get("role")

            user = authenticate(request, username=username, password=password)
            if user is not None and user.role == role:
                login(request, user)
                if role == "professor":
                    return redirect("teacher_home_interface")
                return redirect("student_home_interface")
    
    else:
        form = CustomLoginForm()
    
    return render(request, "polls/login.html", {"form": form})

@login_required
def student_dashboard(request):
    return render(request, "polls/student_home_interface.html")

@login_required
def professor_dashboard(request):
    return render(request, "polls/teacher_home_interface.html")