from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, QuestionForm, PollForm
from django.forms import modelformset_factory
from .models import Poll, Question, CustomUser

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
    polls = Poll.objects.filter(created_by=request.user)
    return render(request, "teacher_home_interface.html")


def create_quiz(request):
    poll_form = PollForm()
    question_formset = QuestionForm(queryset=Question.objects.none())

    if request.method == "POST":
        poll_form = PollForm(request.POST)
        question_formset = QuestionForm(request.POST)

        if poll_form.is_valid() and question_formset.is_valid():
            # Save the poll
            poll = poll_form.save(commit=False)
            poll.created_by = request.user
            poll.save()

            # Save the questions for the poll
            for form in question_formset:
                question = form.save(commit=False)
                question.poll = poll
                question.save()
            
            return redirect("teacher_home_interface") # Redirect to the teacher home interface
    
    return render(request, "quiz_creation.html", {
        'poll_form': poll_form,
        'formset': question_formset
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