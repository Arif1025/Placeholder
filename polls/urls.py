from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('', views.index, name='index'),
    path("login/", login_view, name="login"),
    path("student_home_interface/", student_home_interface, name="student_home_interfaced"),
    path("teacher_home_interface/", teacher_home_interface, name="teacher_home_interface"),
]