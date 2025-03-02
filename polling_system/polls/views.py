from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, QuestionForm
from django.forms import modelformset_factory
from .models import Question
from .models import Quiz

def index(request):
    return HttpResponse("Hello, this is the index view.")

def homepage(request):
    return HttpResponse("Hello! This is the homepage at the root URL.")

def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
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
                messages.error(request, "Invalid username or password.")
    
    else:
        form = CustomLoginForm()
    
    return render(request, "polls/login.html", {"form": form})

@login_required
def student_home_interface(request):
    return render(request, "polls/student_home_interface.html")

@login_required
def teacher_home_interface(request):
    return render(request, "polls/teacher_home_interface.html")

def create_quiz(request):
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=0, can_delete=True)
    formset = QuestionFormSet(request.POST or None, queryset=Question.objects.all())

    if request.method == "POST":
        if "add_question" in request.POST:
            formset = QuestionFormSet(queryset=Question.objects.all())
            formset.extra += 1  # Add an extra form to the set
        elif formset.is_valid():
            formset.save()
            return redirect('create_quiz')  # Redirect after saving
    
    return render(request, "quiz_creation.html", {"formset": formset})

def view_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, "view_quiz.html", {"quiz": quiz})