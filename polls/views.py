from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import TeacherRegistrationForm, TeacherLoginForm, PollForm, QuestionForm, JoinPollForm
from .models import Response, Poll, Question
import csv
from django.contrib import messages

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
            return redirect("login_teacher")  # Redirect to teacher dashboard
    else:
        form = TeacherRegistrationForm()
    return render(request, "register.html", {"form": form})


def login_teacher(request):
    if request.method == "POST":
        form = TeacherLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("teacher_dashboard")
    else:
        form = TeacherLoginForm()
    return render(request, "login.html", {"form": form})

@login_required
def logout_teacher(request):
    logout(request)
    return redirect("login_teacher")  # Redirect to login page after logout

@login_required
def student_dashboard(request):
    return render(request, "student_home_interface.html")

@login_required
def teacher_dashboard(request):
    return render(request, "teacher_home_interface.html")




# ======================= #
# 🚀 Poll CRUD Operations #
# ======================= #
def poll_list(request):
    """List all polls"""
    polls = Poll.objects.all()
    form = PollForm()
    return render(request, "polls/polls.html", {"polls": polls, "form": form})

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

@login_required
def export_poll_responses_csv(request, poll_id):
    """
    View to export poll responses as a CSV file.
    """
    poll = get_object_or_404(Poll, id=poll_id)
    responses = Response.objects.filter(question__poll=poll)

    # Create the HttpResponse object with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{poll.title}_responses.csv"'

    writer = csv.writer(response)
    
    # Write header row
    writer.writerow(["Student", "Question", "Selected Choice", "Submitted At"])

    # Write data rows
    for response_obj in responses:
        writer.writerow([
            response_obj.user.username if response_obj.user else "Anonymous",
            response_obj.question.question_text,
            response_obj.choice.choice_text,
            response_obj.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response
def join_poll_view(request):
    if request.method == 'POST':
        form = JoinPollForm(request.POST)
        if form.is_valid():
            code_entered = form.cleaned_data['code'].strip()
            if not code_entered:
                messages.error(request, "The code you have entered is invalid.")
                return render(request, 'polls/join_poll.html', {'form': form})
            
            try:
                poll = Poll.objects.get(code=code_entered)
                return redirect('question_list', poll_id=poll.id)
            except Poll.DoesNotExist:
                messages.error(request, "The code you have entered is invalid.")
                return render(request, 'polls/join_poll.html', {'form': form})
        else:
            messages.error(request, "The code you have entered is invalid.")
            return render(request, 'polls/join_poll.html', {'form': form})
    
    form = JoinPollForm()
    return render(request, 'polls/join_poll.html', {'form': form})

def question_list(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    questions = poll.questions.all()  
    return render(request, 'polls/question_list.html', {
        'poll': poll,
        'questions': questions
    })
