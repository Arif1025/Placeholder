from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import TeacherRegistrationForm, TeacherLoginForm
from django.contrib.auth.decorators import login_required
from .forms import TeacherRegistrationForm, TeacherLoginForm, PollForm, QuestionForm
from .models import Poll, Question



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


# ======================= #
# 🚀 Poll CRUD Operations #
# ======================= #
def poll_list(request):
    """List all polls"""
    polls = Poll.objects.all()
    form = PollForm()
    return render(request, "polls.html", {"polls": polls, "form": form})

@login_required
def create_poll(request):
    """Create a new poll"""
    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.created_by = request.user  # Assign current user as creator
            poll.save()
            return redirect("poll_list")
    return redirect("poll_list")

@login_required
def update_poll(request, poll_id):
    """Update an existing poll"""
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == "POST":
        form = PollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            return redirect("poll_list")
    else:
        form = PollForm(instance=poll)
    return render(request, "update_poll.html", {"form": form, "poll": poll})

@login_required
def delete_poll(request, poll_id):
    """Delete a poll"""
    poll = get_object_or_404(Poll, id=poll_id)
    poll.delete()
    return redirect("poll_list")

# ========================== #
# 🚀 Question CRUD Operations #
# ========================== #
def question_list(request, poll_id):
    """List all questions for a poll"""
    poll = get_object_or_404(Poll, id=poll_id)
    questions = poll.questions.all()
    form = QuestionForm()
    return render(request, "questions.html", {"poll": poll, "questions": questions, "form": form})

@login_required
def create_question(request, poll_id):
    """Create a question for a poll"""
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.poll = poll
            question.save()
            return redirect("question_list", poll_id=poll.id)
    return redirect("question_list", poll_id=poll.id)

@login_required
def update_question(request, question_id):
    """Update an existing question"""
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect("question_list", poll_id=question.poll.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, "update_question.html", {"form": form, "question": question})

@login_required
def delete_question(request, question_id):
    """Delete a question"""
    question = get_object_or_404(Question, id=question_id)
    poll_id = question.poll.id
    question.delete()
    return redirect("question_list", poll_id=poll_id)
