from django.urls import path
from . import views
from .views import login_view
from .views import student_home_interface
from .views import teacher_home_interface
from .views import create_quiz
from .views import logout_view 
from .views import class_view_teacher  

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
    path('class-view-teacher/', views.class_view_teacher, name='class_view_teacher'), 
    path('class-view-student/', views.class_view_student, name='class_view_student'),
]
