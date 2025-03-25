from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm, QuestionForm, PollForm, JoinPollForm, CustomUserCreationForm
from django.forms import modelformset_factory
import csv
from .models import Poll, Question, Choice, CustomUser, ClassStudent, Class, StudentResponse, StudentQuizResult
from django.contrib.auth.hashers import make_password
import re

def login_view(request):
    form = CustomLoginForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            user = authenticate(request, username=username, password=password)

            if user is not None and user.role == role:
                login(request, user)
                if user.role == 'student':
                    return redirect('student_home_interface')
                elif user.role == 'teacher':
                    return redirect('teacher_home_interface')
            else:
                form.add_error(None, "Invalid username or password")

    return render(request, 'login_interface.html', {'form': form})

@login_required
def student_home_interface(request):
    # Ensure the user is a student
    if not request.user.is_authenticated or request.user.role != 'student':
        return redirect('login_interface')
    
    # Get the polls the student has joined
    joined_polls = request.user.joined_polls.all()

    # Get the classes the student is in
    classes = ClassStudent.objects.filter(student=request.user).select_related('class_instance')

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

    # Get the classes the teacher is teaching
    classes = Class.objects.filter(teacher=request.user)

    # Collect students in each class
    class_students = {}
    for class_instance in classes:
        students = ClassStudent.objects.filter(class_instance=class_instance)
        class_students[class_instance] = [student.student for student in students]

    return render(request, "teacher_home_interface.html", {"polls": quizzes, 'classes': classes, 'class_students': class_students})

@login_required
def create_quiz(request):
    # Remove any existing poll_id in session
    if "poll_id" in request.session:
        del request.session["poll_id"]

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
            return redirect("edit_quiz", poll_id=poll.id)

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

@login_required
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

def question_template(request):
    # Render the question template page
    return render(request, 'question_template.html')

def leave_quiz(request):
    if request.method == "POST":
        return redirect('enter_poll_code')  # Redirect to the enter_poll_code page
    return redirect('enter_poll_code')  # If not POST, redirect anyway

@login_required
def edit_quiz(request, poll_id):
    poll = Poll.objects.filter(id=poll_id).first()
    questions = Question.objects.filter(poll=poll)

    if not poll:
        return redirect("create_quiz")  # Redirect to the create quiz page if poll does not exist

    poll_form = PollForm(instance=poll)
    question_form = QuestionForm()

    if request.method == "POST":
        if "save_quiz" in request.POST:
            poll_form = PollForm(request.POST, instance=poll)
            if poll_form.is_valid():
                poll_form.save()  # Save changes to the poll
                return redirect("teacher_home_interface")  # Redirect to the teacher home interface

        elif "add_question" in request.POST:
            question_text = request.POST.get("question_text", "").strip()
            question_type = request.POST.get("question_type", "").strip()
            correct_answer = request.POST.get("correct_answer", "").strip()

            if not question_text:
                messages.error(request, "Question text cannot be empty.")
                return redirect("edit_quiz", poll_id=poll.id)

            question = Question(poll=poll, text=question_text, question_type=question_type)
                
            # Check if it's an MCQ
            if question.question_type == 'mcq':
                options = request.POST.getlist('options[]')
                correct_option = request.POST.get('correct_option')
                if not options or len(options) < 2:
                    messages.error(request, "Please enter at least 2 options for an MCQ.")
                    return redirect("edit_quiz", poll_id=poll.id)
                
                if correct_option not in options:
                    messages.error(request, "The correct answer must be one of the provided options.")
                    return redirect("edit_quiz", poll_id=poll.id)
                
                question.save()  # Save question before creating choices
                for option_text in options:
                    is_correct = (option_text.strip() == correct_option.strip())  # Mark correct option
                    Choice.objects.create(question=question, text=option_text.strip(), is_correct=is_correct)
            
            # Check if it's a written answer and prompt for answer if empty
            elif question.question_type == 'written':
                correct_answer = request.POST.get('correct_answer', '').strip()
                if not correct_answer:
                    messages.error(request, "Please provide a correct answer.")
                    return redirect("edit_quiz", poll_id=poll.id)
                question.correct_answer = correct_answer
                question.save()
            
            messages.success(request, "Question added successfully.")
            return redirect("edit_quiz", poll_id=poll.id)

    return render(request, "edit_quiz.html", {
        "poll_form": poll_form,
        "question_form": question_form,
        "poll": poll,
        "questions": questions
    })

@login_required
def delete_question(request, poll_id, question_id):
    poll = Poll.objects.filter(id=poll_id).first()
    question = Question.objects.filter(id=question_id, poll=poll).first()

    if not poll or not question:
        messages.error(request, "Invalid question or poll.")
        return redirect("edit_quiz", poll_id=poll_id)

    if Question.objects.filter(poll=poll).count() > 1:  # Prevent deleting the last question
        question.delete()
        messages.success(request, "Question deleted successfully.")
    else:
        messages.error(request, "A poll must have at least one question.")

    return redirect("edit_quiz", poll_id=poll_id)

@login_required
def delete_quiz(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)  # Ensure only creator can delete
    
    if request.method == "POST":
        poll.delete()
        messages.success(request, "Poll deleted successfully.")
    
    return redirect("teacher_home_interface")  # Redirect after deletion

@login_required
def class_view_student(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)
    students = class_instance.participants.filter(id=request.user.id)

    # Ensure the logged-in student is enrolled in the class
    if not ClassStudent.objects.filter(class_instance=class_instance, student=request.user).exists():
        return HttpResponseForbidden("You are not enrolled in this class.")

    # Get all polls for the class
    polls_in_class = Poll.objects.filter(class_instance=class_instance).order_by('-created_at')

    # Get quiz results by the current student for this class
    responses = StudentQuizResult.objects.filter(student=request.user, poll__in=polls_in_class)

    # Calculate average grade for the student in this class
    if responses.exists():
        avg_grade = round(sum(resp.score for resp in responses) / responses.count(), 1)
        num_answered = responses.count()
    else:
        avg_grade = "N/A"
        num_answered = 0

    student_info = {
        'name': request.user.get_full_name() or request.user.username,
        'grade': avg_grade,
        'polls_answered': num_answered,
    }

    # Get most recent poll if exists
    recent_poll = polls_in_class.first()
    recent_poll_title = recent_poll.title if recent_poll else "No polls yet"

    # Calculate average for most recent poll
    if recent_poll:
        recent_poll_responses = StudentQuizResult.objects.filter(poll=recent_poll)
        if recent_poll_responses.exists():
            average_grade = round(sum(resp.score for resp in recent_poll_responses) / recent_poll_responses.count(), 1)
        else:
            average_grade = "N/A"
    else:
        average_grade = "N/A"

    context = {
        'class': class_instance,
        'student': student_info,
        'recent_poll_title': recent_poll_title,
        'average_grade': average_grade,
    }

    return render(request, 'class_template_page_student.html', context)

@login_required
def class_view_teacher(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)

    # Ensure only the teacher who owns this class can access it
    if class_instance.teacher != request.user:
        return HttpResponseForbidden("You do not have permission to view this class.")

    # Get enrolled students
    student_links = ClassStudent.objects.filter(class_instance=class_instance).select_related('student')
    students = []
    for link in student_links:
        student = link.student
        polls_in_class = Poll.objects.filter(class_instance=class_instance)
        responses = StudentQuizResult.objects.filter(student=student, poll__in=polls_in_class)

        if responses.exists():
            avg_grade = round(sum(resp.score for resp in responses) / responses.count(), 1)
            num_answered = responses.count()
        else:
            avg_grade = "N/A"
            num_answered = 0

        students.append({
            'name': student.get_full_name() or student.username,
            'grade': avg_grade,
            'polls_answered': num_answered,
        })

    # Get the most recent poll (if any)
    recent_poll = Poll.objects.filter(class_instance=class_instance).order_by('-created_at').first()
    if recent_poll:
        responses = StudentQuizResult.objects.filter(poll=recent_poll)
        if responses.exists():
            average_grade = round(sum(resp.score for resp in responses) / responses.count(), 1)
        else:
            average_grade = "N/A"
    else:
        average_grade = "N/A"

    context = {
        'class': class_instance,
        'students': students,
        'recent_polls': [recent_poll] if recent_poll else [],
        'average_grade': average_grade,
    }

    return render(request, 'class_template_page_teacher.html', context)

@login_required
def enter_poll_code(request):
    if request.method == 'POST':
        form = JoinPollForm(request.POST)
        if form.is_valid():
            try:
                poll_code = form.cleaned_data['poll_code'] 
                poll = Poll.objects.get(code=poll_code)
                poll.participants.add(request.user)
                return redirect('student_home_interface')
            except Poll.DoesNotExist:
                form.add_error('poll_code', 'Invalid poll code. Please try again.')
                return render(request, 'enter_poll_code.html', {'form': form})
    else:
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
        return redirect('student_home_interface')  # Redirect if not a participant

    # Prepare options for MCQ questions
    questions = poll.questions.all().order_by('id')
    for question in questions:
        if question.question_type == 'mcq':
            question.options_list = list(question.choices.values_list("text", flat=True))  # List MCQ options
        
        # Determine correct answer based on question type
        if question.question_type == 'mcq':
            correct_choice = question.choices.filter(is_correct=True).first()
            correct_answer = correct_choice.text if correct_choice else "No correct option set"
        else:
            correct_answer = question.correct_answer  # Direct correct answer for written questions

        print(f"Question ID: {question.id} -> {question.text}")
        print(f"Correct Answer: {correct_answer}\n")

    return render(request, 'student_view_quiz.html', {'poll': poll, 'questions': questions})  # Render the quiz view for student

@login_required
def end_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)  # Only the poll creator can end it
    if request.method == 'POST':
        poll.is_done = True  # Mark the poll as done
        poll.code = None  # Clear the poll code
        poll.save()
        messages.success(request, f"Poll '{poll.title}' has been ended. Code cleared.")
        return redirect("teacher_home_interface")  # Redirect to teacher's home interface
    return redirect("teacher_home_interface")  # Redirect if not POST request

@login_required
# View for the student confirmation page
def student_confirmation_page(request, poll_code):
    poll = get_object_or_404(Poll, code=poll_code)  # Ensure poll exists

    context = {
        "poll": poll,
        "poll_code": poll_code,
    }
    return render(request, "student_confirmation_page.html", context)  # Render the confirmation page for student

@login_required
def view_poll_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    questions_data = []

    for question in poll.questions.all():
        # Determine the correct answer
        
        correct_choice_text = question.correct_answer

        # Fetch all student responses for the question
        student_responses = StudentResponse.objects.filter(question=question).select_related('student')

        correct_count = 0
        wrong_count = 0
        response_data = []

        for response in student_responses:
            is_correct = False
            is_correct = response.response.strip().lower() == correct_choice_text.strip().lower()

            if is_correct:
                correct_count += 1
            else:
                wrong_count += 1

            # Append response details
            response_data.append({
                'student_name': response.student.get_full_name() or response.student.username,
                'student_response': response.response,
                'is_correct': 'Yes' if is_correct else 'No'
            })

        # Append question data
        questions_data.append({
            'question_text': question.text,
            'correct_choice': correct_choice_text,
            'correct_count': correct_count,
            'wrong_count': wrong_count,
            'responses': response_data
        })

    return render(request, 'charts.html', {
        'poll': poll,
        'questions_data': questions_data
    })

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        print(f"Received data - Username: {username}, Role: {role}")  # Debug log

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "register.html")
        
        if not username or not password or not confirm_password or not role:
            messages.error(request, "All fields are required.")
            return render(request, "register.html")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, "register.html")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, "register.html")

        if not re.search(r"\d", password):
            messages.error(request, "Password must contain at least one number.")
            return render(request, "register.html")
        

        # Create the user
        user = CustomUser.objects.create_user(username=username, password=password)
        user.role = role
        user.save()

        print(f"User created: {user.username} - Role: {user.role}")  # Debug log

        # Log in the user and redirect to home
        user = authenticate(request, username=username, password=password)
        if user:
            print(f"User authenticated: {user.username}")  # Debug log    
            login(request, user)
            if user.role == 'student':
                return redirect('student_home_interface')
            elif user.role == 'teacher':
                return redirect('teacher_home_interface')
        else:
            print("Authentication failed!")  # Debug log
            messages.error(request, "Something went wrong. Please try logging in manually.")
            return redirect("login_interface")

    return render(request, "register.html")  # Render the registration page

def polls_list(request):
    polls = Poll.objects.all()  # Fetch all polls
    return render(request, 'polls/polls.html', {'polls': polls})  # Render the polls list page

def export_poll_responses(request, poll_id):
    # Get the poll or return a 404 if not found
    poll = get_object_or_404(Poll, id=poll_id)
    
    # Get all student responses and results for the poll
    student_results = StudentQuizResult.objects.filter(poll=poll)

    # Create a response object and set headers for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{poll.title}_responses.csv"'

    # Write to CSV
    writer = csv.writer(response)

    writer.writerow(['Student', 'Score', 'Total Questions', 'Score Percentage', 'Submitted At'])

    for result in student_results:
        score_percentage = round((result.score / result.total_questions) * 100, 2) if result.total_questions > 0 else 0
        writer.writerow([
            result.student.username,
            result.score,
            result.total_questions,
            f"{score_percentage}%",
            result.submitted_at
        ])

    return response


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print("Existing usernames:", list(CustomUser.objects.values_list("username", flat=True)))  # Debug log
        print("Entered username:", username)
        
        try:
            user = CustomUser.objects.get(username=username)
            request.session['reset_username'] = username
            return redirect('reset_password')  # Redirect to reset password page
        except CustomUser.DoesNotExist:
            messages.error(request, "No account found with this username.")
            return render(request, 'forgot_password.html', {'form_error': True})

    return render(request, 'forgot_password.html')  # Render the forgot password page

def reset_password(request):
    if "reset_username" not in request.session:
        messages.error(request, "No username provided for password reset.")
        return redirect("forgot_password")    
    
    username = request.session['reset_username']
    
    if not username:
        messages.error(request, "Session expired. Please request password reset again.")
        return redirect('forgot_password')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validate password length and numeric character requirement
        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'reset_password.html')

        if not re.search(r'\d', password1):
            messages.error(request, "Password must contain at least one number.")
            return render(request, 'reset_password.html')


        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'reset_password.html')
        try:
            user = CustomUser.objects.get(username=username)
            user.password = make_password(password1)
            user.save()
            messages.success(request, "Password successfully updated. You can now log in.")
            del request.session["reset_username"]  # Remove username from session
            return redirect("login_interface")  # Redirect to login page
        except CustomUser.DoesNotExist:
            request.session.pop('reset_username', None)
            return redirect('login_interface')

    return render(request, 'reset_password.html')  # Render the reset password page

@login_required
def submit_quiz(request, poll_code):
    poll = get_object_or_404(Poll, code=poll_code)
    print(f"Poll Code: {poll.code}")  # Debug log to check which poll is being accessed

    # Ensure the student is a participant in this poll
    if request.user not in poll.participants.all():
        return redirect('student_home_interface')  # Redirect if the user is not a participant

    if request.method == "POST":
        score = 0  # Initialize the student's score
        total_questions = poll.questions.count()  # Total number of questions in the poll
        student_answers = []  # List to store all the student's responses for session storage

        # Iterate over all the questions in the poll
        for question in poll.questions.all():
            student_answer = request.POST.get(f"question_{question.id}", "").strip()  # Get student's answer
            is_correct = False  # Default assumption: the student's answer is incorrect

            # If the question is multiple-choice (MCQ), check if the answer is correct
            if question.question_type == "mcq":
                correct_choice = question.choices.filter(is_correct=True).first()  # Find the correct choice
                print(f"DEBUG: Processing MCQ - {question.text} | Correct Choice: {correct_choice.text if correct_choice else 'None'}")
                # If the student's answer matches the correct choice, it's correct
                if correct_choice and student_answer == correct_choice.text:
                    is_correct = True
                    score += 1  # Increase score for correct answers

            # If the question is a written answer, check if the answer matches the correct answer
            elif question.question_type == "written":
                # Store the student's written response in the database
                StudentResponse.objects.create(
                    student=request.user,
                    question=question,
                    response=student_answer
                )
                # Check if the student's answer is correct
                is_correct = student_answer.lower() == question.correct_answer.lower()
                if is_correct:
                    score += 1  # Increase score for correct answers
                print(f"DEBUG: Text Question - {question.text} | Stored Correct Answer: {question.correct_answer}")

            # Determine the correct answer to store, depending on the question type
            correct_answer_value = question.correct_answer if question.question_type == "written" else (correct_choice.text if correct_choice else "No correct answer set")
            print(f"DEBUG: Storing Question - {question.text} | Correct Answer: {correct_answer_value}")

            # Append the student's answer and correctness info to the answers list
            student_answers.append({
                'question': question.text,
                'user_answer': student_answer,
                'correct_answer': correct_answer_value,
                'is_correct': is_correct
            })

        # Store the student's quiz result in the database
        StudentQuizResult.objects.create(
            student=request.user,
            poll=poll,
            score=score,
            total_questions=total_questions
        )

        # Store the results in the session for the final score page
        request.session['quiz_results'] = {
            'poll_code': poll_code,
            'score_percentage': round((score / total_questions) * 100) if total_questions > 0 else 0,  # Calculate percentage
            'correct_count': score,
            'total_questions': total_questions,
            'student_answers': student_answers
        }

        # Debug log to print out all the student's answers before saving to session
        print("\n==== DEBUG: Final Student Answers Before Saving to Session ====")
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(student_answers)

        # Redirect the student to the confirmation page
        return redirect("student_confirmation_page", poll_code=poll.code)  

    # If it's not a POST request, redirect to the quiz view page to start the quiz
    if poll_code:
        return redirect("student_view_quiz", poll_code=poll_code)
    else:
        return redirect("student_home_interface")  # If no poll code, redirect to the student's home interface
