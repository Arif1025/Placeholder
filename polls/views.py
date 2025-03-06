from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, QuestionForm
from django.forms import modelformset_factory
from .models import Question

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
    return render(request, "teacher_home_interface.html")

def create_quiz(request):
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=0, can_delete=True)
    formset = QuestionFormSet(request.POST or None, queryset=Question.objects.all())

    if request.method == "POST":
        if "add_question" in request.POST:
            formset = QuestionFormSet(queryset=Question.objects.all())
            formset.extra += 1  
        elif formset.is_valid():
            formset.save()
            return redirect('create_quiz') 
    
    return render(request, "quiz_creation.html", {"formset": formset})

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

def class_view_teacher(request):
    class_name = request.GET.get('class_name')  
    if not class_name:
        return HttpResponse("Class not found.", status=404)
    return render(request, 'class_template_page_teacher.html', {'class_name': class_name})

def class_view_student(request):
    class_name = request.GET.get('class_name')
    if not class_name:
        return HttpResponse("Class not found.", status=404) 
    return render(request, 'class_template_page_student.html', {'class_name': class_name})