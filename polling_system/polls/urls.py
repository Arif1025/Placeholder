from django.urls import path
from . import views
from .views import login_view
from .views import student_home_interface
from .views import teacher_home_interface
from .views import create_quiz

urlpatterns = [
    path('', views.index, name='index'),
    path("login_interface/", login_view, name="login_interface"),
    path("student_home_interface/", student_home_interface, name="student_home_interface"),
    path("teacher_home_interface/", teacher_home_interface, name="teacher_home_interface"),
    path("create-quiz/", create_quiz, name="create_quiz"),
    path('download-report/', views.download_report, name='download_report'),
]