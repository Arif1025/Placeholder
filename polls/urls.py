from django.urls import path
from . import views
from .views import login_view
from .views import student_home_interface
from .views import teacher_home_interface
from .views import create_quiz
from .views import logout_view
from .views import edit_quiz, edit_question, delete_question

urlpatterns = [
    path('', views.index, name='index'),
    path("login_interface/", login_view, name="login_interface"),
    path("student_home_interface/", student_home_interface, name="student_home_interface"),
    path("teacher_home_interface/", teacher_home_interface, name="teacher_home_interface"),
    path("create-quiz/", create_quiz, name="create_quiz"),
    path("logout/", logout_view, name="logout"), 
    path("final-score/", views.final_score_page, name="final_score_page"),
    path('student-home/', views.student_home_interface, name='student_home_interface'),
    path('quiz/', views.question_template, name='question_template'),
    path('polls/edit/<int:poll_id>/', edit_quiz, name='edit_quiz'),
    path("edit_question/<int:question_id>/", edit_question, name="edit_question"),
    path('polls/delete_question/<int:question_id>/<int:poll_id>/', views.delete_question, name='delete_question')
]