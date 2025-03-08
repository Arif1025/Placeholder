from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, QuestionForm, PollForm
from django.forms import modelformset_factory
from .models import Poll, Question, Choice, CustomUser

def index(request):
    return HttpResponse("Hello, this is the index view.")

def homepage(request):
    return HttpResponse("Hello! This is the homepage at the root URL.")


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user role
            if user.role == 'student':
                return redirect('student_home_interface')
            elif user.role == 'teacher':
                return redirect('teacher_home_interface')
        else:
            # Handle invalid login
            return render(request, 'login_interface.html', {'error': 'Invalid username or password'})
    return render(request, 'login_interface.html')


@login_required
def student_home_interface(request):
    return render(request, "student_home_interface.html")

@login_required
def teacher_home_interface(request):
    quizzes = Poll.objects.all()
    return render(request, "teacher_home_interface.html", {"polls": quizzes})

@login_required
def create_quiz(request):
    poll_id = request.session.get("poll_id")
    poll = Poll.objects.filter(id=poll_id).first() if poll_id else None

    poll_form = PollForm()
    question_form = QuestionForm()
    
    if request.method == "POST":
        if "save_quiz" in request.POST:
            poll_form = PollForm(request.POST)
            if poll_form.is_valid():
                poll = poll_form.save(commit=False)
                poll.created_by = request.user
                poll.save()
                request.session["poll_id"] = poll.id  # Store poll ID in session

                return redirect("create_quiz")  # Redirect so the question form appears

        elif "add_question" in request.POST and poll:
            question_form = QuestionForm(request.POST)
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.poll = poll
                question.save()
                return redirect("create_quiz")  # Stay on page to add more questions

    questions = Question.objects.filter(poll=poll) if poll else []


    return render(request, "create_quiz.html", {
        "poll_form": poll_form,
        "question_form": question_form if poll else None,  # Only show if poll exists
        "poll": poll,
        "questions": questions
    })
    
def logout_view(request):
    logout(request)  # Log out the user
    return redirect('login_interface')  # Redirect to the login page

def final_score_page(request):
    # Any logic for final score
    return render(request, "final_score_page.html")

# View for the student home interface page
def student_home_interface(request):
    return render(request, 'student_home_interface.html')

# View for the question template page
def question_template(request):
    return render(request, 'question_template.html')

@login_required
def edit_quiz(request, poll_id):
    poll = Poll.objects.filter(id=poll_id).first()

    if not poll:
        return redirect("create_quiz")  # Redirect to the create quiz page if poll does not exist

    poll_form = PollForm(instance=poll)
    question_form = QuestionForm()

    if request.method == "POST":
        if "save_quiz" in request.POST:
            poll_form = PollForm(request.POST, instance=poll)
            if poll_form.is_valid():
                poll_form.save()  # Save changes to the poll
                return redirect("edit_quiz", poll_id=poll.id)  # Reload page to show updated poll details

        elif "add_question" in request.POST:
            question_form = QuestionForm(request.POST)
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.poll = poll
                question.save()
                return redirect("edit_quiz", poll_id=poll.id)  # Stay on page to add more questions

    questions = Question.objects.filter(poll=poll)

    return render(request, "edit_quiz.html", {
        "poll_form": poll_form,
        "question_form": question_form,
        "poll": poll,
        "questions": questions
    })