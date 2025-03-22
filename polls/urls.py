from django.urls import path
from . import views
from .views import login_view
from .views import student_home_interface
from .views import teacher_home_interface
from .views import create_quiz
from .views import logout_view
from .views import edit_quiz, edit_question, delete_question, delete_quiz
from .views import logout_view 
from .views import leave_quiz


urlpatterns = [
    path('', views.index, name='index'),
    path("login_interface/", login_view, name="login_interface"),
    path("student_home_interface/", views.student_home_interface, name="student_home_interface"),
    path("teacher_home_interface/", teacher_home_interface, name="teacher_home_interface"),
    path("create-quiz/", create_quiz, name="create_quiz"),
    path("logout/", logout_view, name="logout"), 
    path("final-score/", views.final_score_page, name="final_score_page"),
    path('quiz/', views.question_template, name='question_template'),
    path('polls/edit/<int:poll_id>/', edit_quiz, name='edit_quiz'),
    path("edit_question/<int:question_id>/", edit_question, name="edit_question"),
    path('polls/delete_question/<int:question_id>/<int:poll_id>/', views.delete_question, name='delete_question'),
    path("polls/delete/<int:poll_id>/", delete_quiz, name="delete_quiz"),
    path('class-view-teacher/<int:class_id>/', views.class_view_teacher, name='class_view_teacher'), 
    path('class-view-student/', views.class_view_student, name='class_view_student'),
    path('enter-poll-code/', views.enter_poll_code, name='enter_poll_code'),
    path('quiz/<int:poll_id>/', views.teacher_view_quiz, name='teacher_view_quiz'),
    path('quiz/<str:poll_code>/student/', views.student_view_quiz, name='student_view_quiz'),
    path('leave-quiz/', leave_quiz, name='leave_quiz'),
    path('student-confirmation/', views.student_confirmation_page, name='student_confirmation_page'),
    path('polls/results/<int:poll_id>/', views.view_poll_results, name='view_poll_results'),
    path('polls/<int:poll_id>/end/', views.end_poll, name='end_poll'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('', views.polls_list, name='polls_list'),
    path('export_poll_responses/<int:poll_id>/', views.export_poll_responses, name='export_poll_responses'),
]
