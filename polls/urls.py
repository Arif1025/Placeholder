from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('', views.index, name='index'),
    path("login/", login_view, name="login"),
    path("student-dashboard/", student_dashboard, name="student_dashboard"),
    path("professor-dashboard/", professor_dashboard, name="professor_dashboard"),
]