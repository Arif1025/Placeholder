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

"""
@login_required
def create_quiz(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        #formset = QuestionFormSet(request.POST)
        
        if form.is_valid(): #and formset.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            #questions = formset.save(commit=False)

            questions_data = request.POST.getlist("questions")  
            for question_text in questions_data:
                question = Question(poll=quiz, text=question_text)
                question.save()
                #formset.save_m2m()

            return redirect('teacher_home_interface')  # Redirect to teacher home after saving
        else:
            print(form.errors)  #For debugging
            #print(formset.errors)  #For debugging
    else:
        form = PollForm()
        #formset = QuestionFormSet()

    return render(request, 'create_quiz.html', {'form': form})#, 'formset': formset})
"""
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
                request.session["poll_id"] = poll.id  # ✅ Store poll ID in session

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