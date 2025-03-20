from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, QuestionForm, PollForm, JoinPollForm, CustomUserCreationForm
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
    # Get the polls the student has joined
    joined_polls = request.user.joined_polls.all()    
    
    return render(request, "student_home_interface.html",  {'joined_polls': joined_polls})

@login_required
def teacher_home_interface(request):
    quizzes = Poll.objects.all()
    return render(request, "teacher_home_interface.html", {"polls": quizzes})

@login_required
def create_quiz(request):
    poll_id = request.session.pop("poll_id", None)  # Get poll ID from session
    poll = None
    poll_form = PollForm()
    question_form = QuestionForm()
    
    if request.method == "POST" and "save_quiz" in request.POST:
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            request.session["poll_id"] = poll.id
            return redirect("teacher_home_interface")

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

# View for leave_quiz view
def leave_quiz(request):
    if request.method == "POST":  # Handle the POST request when the form is submitted
        return redirect('enter_poll_code')  # Redirect to the enter_poll_code page
    return redirect('enter_poll_code')


@login_required
def edit_quiz(request, poll_id):
    poll = Poll.objects.filter(id=poll_id).first()

    if not poll:
        return redirect("create_quiz")  # Redirect to the create quiz page if poll does not exist

    poll_form = PollForm(instance=poll)
    question_form = QuestionForm()

    if request.method == "POST":
        if "save_quiz" in request.POST:
            print("✅ Save Quiz button clicked in edit!")  # Debugging log
            print("POST data:", request.POST)  # Log the entire POST data
            poll_form = PollForm(request.POST, instance=poll)
            if poll_form.is_valid():
                poll_form.save()  # Save changes to the poll
                print("✅ Redirecting to teacher_home_interface...")  # Debugging log
                return redirect("teacher_home_interface")  # Redirect to the teacher home interface
            else:
                print("❌ Form is invalid. Errors:", poll_form.errors.as_json())  # Debugging log

        elif "add_question" in request.POST:
            question_form = QuestionForm(request.POST)
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.poll = poll
                question.save()
                return redirect("edit_quiz", poll_id=poll.id)  # Stay on page to add more questions
        
        elif "delete_question" in request.POST:
            question_id = request.POST.get("question_id")
            if question_id:
                question = Question.objects.get(id=question_id)
                if questions.count() > 1:  # Prevent deleting last question
                    question.delete()
                else:
                    messages.error(request, "A poll must have at least one question.")

    questions = Question.objects.filter(poll=poll)

    return render(request, "edit_quiz.html", {
        "poll_form": poll_form,
        "question_form": question_form,
        "poll": poll,
        "questions": questions
    })

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, poll__created_by=request.user)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect("edit_quiz")

    else:
        form = QuestionForm(instance=question)

    return render(request, "edit_question.html", {"form": form, "question": question})

@login_required
def delete_question(request, question_id, poll_id):
    question = get_object_or_404(Question, id=question_id, poll__created_by=request.user)
    poll_id = question.poll.id
    question.delete()
    return redirect("edit_quiz", poll_id=poll_id)

@login_required
def delete_quiz(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)  # Ensure only creator can delete
    
    if request.method == "POST":
        poll.delete()
        messages.success(request, "Poll deleted successfully.")
    
    return redirect("teacher_home_interface")  # Redirect after deletion

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

@login_required
def enter_poll_code(request):
<<<<<<< HEAD
    print("Enter poll code view is being called")  # Debug log
    if request.method == 'POST':
        print("POST data recieved:", request.POST)  # Debug log
        form = JoinPollForm(request.POST)
        if form.is_valid():
            poll_code = form.cleaned_data['poll_code']
            try:
                print(f"Looking for poll with code: {poll_code}")  # Debug log                
                poll = Poll.objects.get(code=poll_code)
                print(f"Poll found: {poll.title}")  # Debug log                

                poll.participants.add(request.user)
                print(f"User {request.user.username} added to poll {poll.title}")  # Debug log

                # Redirect back to student home interface with success message
                return redirect('student_home_interface')
            except Poll.DoesNotExist:
                print("Poll not found")  # Debug log
                form.add_error('poll_code', 'Invalid poll code. Please try again.')
        else:
            print(form.errors)
    else:
        print("GET request recieved")  # Debug log
        form = JoinPollForm()

    return render(request, 'enter_poll_code.html', {'form': form})

@login_required
def teacher_view_quiz(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    questions = Question.objects.filter(poll=poll)

    return render(request, 'teacher_view_quiz.html', {'poll': poll, 'questions': questions})

@login_required
def student_view_quiz(request, poll_code):
    poll = get_object_or_404(Poll, code=poll_code)
    
    # Check if the student is a participant in this poll
    if request.user not in poll.participants.all():
        return redirect('student_home_interface')

    # Render the poll's questions
    return render(request, 'student_view_quiz.html', {'poll': poll})
=======
    if request.method == 'POST':
        poll_code = request.POST.get('pollCode')
        if poll_code:
            try:
                poll = Poll.objects.get(code=poll_code, is_done=False)
                return redirect('question_template', poll_id=poll.id)
            except Poll.DoesNotExist:
                return render(request, 'enter_poll_code.html', {'error': 'Invalid or inactive poll code'})
    return render(request, 'enter_poll_code.html')
>>>>>>> poll_code


@login_required
def end_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)
    if request.method == 'POST':
        poll.is_done = True
        poll.code = None  
        poll.save()
        messages.success(request, f"Poll '{poll.title}' has been ended. Code cleared.")
        return redirect("teacher_home_interface")
    return redirect("teacher_home_interface")  

# View for the student confirmation page
def student_confirmation_page(request):
    return render(request, 'student_confirmation_page.html')


@login_required
def view_poll_results(request, poll_id):
    # Fetch the poll based on the poll_id
    poll = get_object_or_404(Poll, id=poll_id)

    # Fetch related data
    questions = Question.objects.filter(poll=poll)
    choices = Choice.objects.filter(question__in=questions)

    # Pass data to the chart template
    return render(request, 'charts.html', {
        'poll': poll,
        'questions': questions,
        'choices': choices,
    })

def register_view(request):
<<<<<<< HEAD
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            messages.success(request, "Registration successful!")
            return redirect("dashboard")  # Change to your desired redirect page
=======
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        
        User = get_user_model()
        user = User.objects.create_user(username=username, password=password)
        
        user.role = role
        user.save()
        
        # Set user role if using a custom user model
        if hasattr(user, 'customuser'):  
            user.customuser.role = role
            user.customuser.save()

        # Authenticate and login the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Redirect to the appropriate home interface
            if role == 'student':
                return redirect('student_home_interface')
            elif role == 'teacher':
                return redirect('teacher_home_interface')
>>>>>>> poll_code
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})

def forgot_password_view(request):
    return render(request, 'forgot_password.html')