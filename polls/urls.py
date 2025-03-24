from django.urls import path
from . import views
from .views import login_view
from .views import student_home_interface
from .views import teacher_home_interface
from .views import create_quiz
from .views import logout_view
from .views import edit_quiz, delete_question, delete_quiz
from .views import logout_view 
from .views import leave_quiz
from .views import student_view_quiz, submit_quiz

urlpatterns = [
    # Login view, allows users to log in
    path("login_interface/", login_view, name="login_interface"),

    # Student's home interface, view for students after login
    path("student_home_interface/", views.student_home_interface, name="student_home_interface"),

    # Teacher's home interface, view for teachers after login
    path("teacher_home_interface/", teacher_home_interface, name="teacher_home_interface"),

    # Create a new quiz, view to create a poll or quiz
    path("create-quiz/", create_quiz, name="create_quiz"),

    # Logout view, allows users to log out of the system
    path("logout/", logout_view, name="logout"), 

    # Final score page, view for displaying the final score for a poll
    path("final-score/<str:poll_code>/", views.final_score_page, name="final_score_page"),

    # Template for a quiz question page
    path('quiz/', views.question_template, name='question_template'),

    # Edit a quiz, view to modify a poll or quiz details
    path('polls/edit/<int:poll_id>/', edit_quiz, name='edit_quiz'),

    # Delete a specific question from a quiz
    path("quiz/<int:poll_id>/delete_question/<int:question_id>/", delete_question, name="delete_question"),

    # Delete a poll/quiz
    path("polls/delete/<int:poll_id>/", delete_quiz, name="delete_quiz"),

    # View a class as a teacher, teacher's view of a class
    path('class-view-teacher/<int:class_id>/', views.class_view_teacher, name='class_view_teacher'), 

    # View a class as a student, student's view of a class
    path('class-view-student/<int:class_id>/', views.class_view_student, name='class_view_student'),

    # Enter poll code, page for entering a poll code to join
    path('enter-poll-code/', views.enter_poll_code, name='enter_poll_code'),

    # Teacher's view of a quiz/poll
    path('quiz/<int:poll_id>/', views.teacher_view_quiz, name='teacher_view_quiz'),

    # Student's view of a quiz/poll using the poll code
    path('quiz/<str:poll_code>/student/', views.student_view_quiz, name='student_view_quiz'),

    # Leave a quiz, allows the student to leave the quiz
    path('leave-quiz/', leave_quiz, name='leave_quiz'),

    # Student confirmation page, page confirming student participation in a poll
    path('student-confirmation/<str:poll_code>/', views.student_confirmation_page, name='student_confirmation_page'),

    # View results for a poll, page for viewing poll results
    path('polls/results/<int:poll_id>/', views.view_poll_results, name='view_poll_results'),

    # End the poll, allows poll to be ended by a teacher
    path('polls/<int:poll_id>/end/', views.end_poll, name='end_poll'),

    # Registration page for new users
    path('register/', views.register_view, name='register'),

    # Forgot password page, allows users to reset their passwords
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    # Reset password page, view for resetting a user's password
    path('reset-password/', views.reset_password, name='reset_password'),

    # Poll list view, shows a list of all available polls
    path('', views.polls_list, name='polls_list'),

    # Export poll responses, allows exporting responses for a poll
    path('export_poll_responses/<int:poll_id>/', views.export_poll_responses, name='export_poll_responses'),

    # Submit quiz, allows a student to submit their quiz responses
    path('submit_qui/<str:poll_code>/submit/', submit_quiz, name='submit_quiz'),
]
