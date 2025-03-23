from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, QuestionForm, PollForm, JoinPollForm, CustomUserCreationForm
from django.forms import modelformset_factory
import csv
from .models import Poll, Question, Choice, CustomUser, Response, ClassStudent, Class, StudentResponse, StudentQuizResult
from django.contrib.auth.hashers import make_password
import re


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
    print("student_home_interface view called") # Debug log
    print("Request user:", request.user) # Debug log
    print("User role:", request.user.role) # Debug log

    # If the user isn't authenticated or isn't a student, redirect to login
    if not request.user.is_authenticated or request.user.role != 'student':
        return redirect('login_interface')
    
    # Get the polls the student has joined
    joined_polls = request.user.joined_polls.all()

    # Get the classes that the student is in
    classes = ClassStudent.objects.filter(student=request.user).select_related('class_instance')

    # Debugging print
    print("Logged in student:", request.user)
    print("Classes fetched for student:", classes)
    print("Number of classes:", classes.count())

    # Collect teachers for each class
    class_teachers = {}
    for class_student in classes:
        teacher = class_student.class_instance.teacher
        class_teachers[class_student.class_instance] = teacher

    return render(request, "student_home_interface.html",  {
        'joined_polls': joined_polls,
        'classes': classes,
        'class_teachers': class_teachers
    })

@login_required
def teacher_home_interface(request):
    # Get all polls created by the teacher
    quizzes = Poll.objects.all()

    # Get the classes that the teacher is teaching
    classes = Class.objects.filter(teacher=request.user)

    # Collect students in each class
    class_students = {}
    for class_instance in classes:
        students = ClassStudent.objects.filter(class_instance=class_instance)
        class_students[class_instance] = [student.student for student in students]


    return render(request, "teacher_home_interface.html", {"polls": quizzes,'classes': classes,
        'class_students': class_students})

@login_required
def create_quiz(request):
    poll_id = request.session.get("poll_id")  # Get poll ID from session
    poll = Poll.objects.filter(id=poll_id).first() if poll_id else None
    poll_form = PollForm(instance=poll) if poll else PollForm() 
    question_form = QuestionForm() if poll else None
    questions = []
    
    if request.method == "POST" and "save_quiz" in request.POST:
        poll_form = PollForm(request.POST, instance=poll)
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
                question.correct_answer = request.POST.get('correct_answer')
                question.save()

                options = request.POST.getlist("options[]")
                for option_text in options:
                    if option_text.strip():
                        Choice.objects.create(question=question, text=option_text.strip())

                return redirect("create_quiz")  # Stay on page to add more questions

    elif "poll_id" in request.GET:
        poll = get_object_or_404(Poll, id=request.GET["poll_id"])
        questions = poll.questions.all()

    return render(request, "create_quiz.html", {
        "poll_form": poll_form,
        "question_form": question_form if poll else None,  # Only show if poll exists
        "poll": poll,
        "questions": questions
    })
    
def logout_view(request):
    logout(request)  # Log out the user
    return redirect('login_interface')  # Redirect to the login page

def final_score_page(request, poll_code):
    quiz_results = request.session.get('quiz_results', None)
    poll = get_object_or_404(Poll, code=poll_code)

    student_result = StudentQuizResult.objects.filter(student=request.user, poll=poll).first()

    context = {
        "poll": poll,
        "poll_code": poll_code,
        "student_result": student_result,
        "quiz_results": quiz_results
    }
    if not quiz_results:
         return redirect('student_home_interface')  # Redirect if no results found
    
    return render(request, "final_score_page.html", context)

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
                
                # Check if it's an MCQ
                if question.question_type == 'mcq':
                    options = request.POST.get('options', '').strip()
                    if not options:
                        messages.error(request, "Please enter at least one option for an MCQ.")
                        return redirect("edit_quiz", poll_id=poll.id)
                    
                    question.save()  # Save question before creating choices
                    for option_text in options.split(','):
                        Choice.objects.create(question=question, text=option_text.strip())
                
                # Check if it's a written answer and prompt for answer if empty
                elif question.question_type == 'written':
                    options  = request.POST.get('options', '').strip()
                    if not options:
                        messages.error(request, "Please provide a written answer.")
                        return redirect("edit_quiz", poll_id=poll.id)
                    question.options = options
                
                question.save()
                messages.success(request, "Question added successfully.")
                return redirect("edit_quiz", poll_id=poll.id)
        
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

def class_view_teacher(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)
    students = CustomUser.objects.filter(classstudent__class_instance=class_instance, role="student")
    context = {
        'class': class_instance,
        'students': students,
    }
    return render(request, 'class_template_page_teacher.html', context)

def class_view_student(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)

    students = CustomUser.objects.filter(classstudent__class_instance=class_instance)

    return render(request, 'class_template_page_student.html', {
        'class_name': class_instance.name,
        'teacher': class_instance.teacher,  # Assuming there's a teacher field
        'students': students,
    })

@login_required
def enter_poll_code(request):

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
    questions = Question.objects.filter(poll=poll).prefetch_related('choices')

    questions_with_choices = []

    for question in questions:
        choices = list(question.choices.all())
        choice_labels = list(zip("abcdefghijklmnopqrstuvwxyz", choices))
    
        # Debugging: Print choices
        print(f"Question: {question.text}")
        for letter, choice in choice_labels:
            print(f"{letter}) {choice.text}")
        
        questions_with_choices.append({
            'question': question,
            'choice_labels': choice_labels
        })

    return render(request, 'teacher_view_quiz.html', {'poll': poll, 'questions_with_choices': questions_with_choices})

@login_required
def student_view_quiz(request, poll_code):
    poll = get_object_or_404(Poll, code=poll_code)
    
    # Check if the student is a participant in this poll
    if request.user not in poll.participants.all():
        return redirect('student_home_interface')

    # Prepare options for MCQ questions
    questions = poll.questions.all()
    for question in questions:
        if question.question_type == 'mcq':
            question.options_list = list(question.choices.values_list("text", flat=True))

    return render(request, 'student_view_quiz.html', {'poll': poll, 'questions': questions})

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
def student_confirmation_page(request, poll_code):
    poll = get_object_or_404(Poll, code=poll_code)  # Ensure poll exists

    context = {
        "poll": poll,
        "poll_code": poll_code,
    }
    return render(request, "student_confirmation_page.html", context)


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
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            login(request, user)
            return redirect("login")  # Redirect to login page after registration
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})

def polls_list(request):
    polls = Poll.objects.all()
    return render(request, 'polls/polls.html', {'polls': polls})

def export_poll_responses(request, poll_id):
    # Get the poll or return a 404 if not found
    poll = get_object_or_404(Poll, id=poll_id)
    
    # Get all responses for the poll
    responses = Response.objects.filter(question__poll=poll)
    
    # Create a response object and set headers for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{poll.title}_responses.csv"'

    # Write to CSV
    writer = csv.writer(response)
    writer.writerow(['Username', 'Question', 'Choice', 'Submitted At'])

    for resp in responses:
        writer.writerow([resp.user.username if resp.user else 'Anonymous', resp.question.text, resp.choice.choice_text, resp.submitted_at])

    return response

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect('forgot_password')

        request.session['reset_email'] = email
        return redirect('reset_password')  # Redirect to reset password page

    return render(request, 'forgot_password.html')

def reset_password(request):
    email = request.session.get('reset_email')
    
    if not email:
        messages.error(request, "Session expired. Please request password reset again.")
        return redirect('forgot_password')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validate password length and numeric character requirement
        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('reset_password')

        if not re.search(r'\d', password1):  # Checks if the password has at least one number
            messages.error(request, "Password must contain at least one number.")
            return redirect('reset_password')


        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')

        user = CustomUser.objects.get(email=email)
        user.password = make_password(password1)
        user.save()

        messages.success(request, "Password reset successful! You can now log in.")
        request.session.pop('reset_email', None)
        return redirect('login_interface')

    return render(request, 'reset_password.html')

@login_required
def submit_quiz(request, poll_code):
    poll = get_object_or_404(Poll, code=poll_code)
    print(f"Poll Code: {poll.code}") # Debug log

    # Ensure the student is a participant
    if request.user not in poll.participants.all():
        return redirect('student_home_interface')

    if request.method == "POST":
        score = 0  # Track student score
        total_questions = poll.questions.count()
        student_answers = []  # Store student responses for session

        for question in poll.questions.all():
            student_answer = request.POST.get(f"question_{question.id}", "").strip()

            is_correct = False  # Default to incorrect

            # If MCQ, check if the answer is correct
            if question.question_type == "mcq":
                correct_choice = question.choices.filter(is_correct=True).first()
                if correct_choice and student_answer == correct_choice.text:
                    is_correct = True
                    score += 1  # Increase score for correct answers

            # If Text-based, save the student's response
            elif question.question_type == "text":
                StudentResponse.objects.create(
                    student=request.user,
                    question=question,
                    response=student_answer
                )
                is_correct = student_answer.lower() == question.correct_answer.lower()

                if is_correct:
                    score += 1  # Increase score for correct text answers

            # Store student answer for final score page
            student_answers.append({
                'question': question.text,
                'user_answer': student_answer,
                'correct_answer': question.correct_answer if question.question_type == "text" else (correct_choice.text if correct_choice else "No correct answer set"),
                'is_correct': is_correct
            })

        # Store student score in database
        StudentQuizResult.objects.create(
            student=request.user,
            poll=poll,
            score=score,
            total_questions=total_questions
        )

        # Store results in session for final score page
        request.session['quiz_results'] = {
            'poll_code': poll_code,
            'score_percentage': round((score / total_questions) * 100) if total_questions > 0 else 0,
            'correct_count': score,
            'total_questions': total_questions,
            'student_answers': student_answers
        }

        return redirect("student_confirmation_page", poll_code=poll.code)  # Redirect to confirmation page

    if poll_code:
        return redirect("student_view_quiz", poll_code=poll_code)
    else:
        return redirect("student_home_interface")