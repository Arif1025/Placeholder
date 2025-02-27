from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("homepage/", homepage, name="homepage"),
    path("register/", register_teacher, name="register_teacher"),
    path("login/", login_teacher, name="login_teacher"),
    path("logout/", logout_teacher, name="logout_teacher"),
    path("teacher-dashboard/", teacher_dashboard, name="teacher_dashboard"),
    path("polls/", poll_list, name="poll_list"),
    path("polls/create/", create_poll, name="create_poll"),
    path("polls/<int:poll_id>/update/", update_poll, name="update_poll"),
    path("polls/<int:poll_id>/delete/", delete_poll, name="delete_poll"),

    path("polls/<int:poll_id>/questions/", question_list, name="question_list"),
    path("polls/<int:poll_id>/questions/create/", create_question, name="create_question"),
    path("questions/<int:question_id>/update/", update_question, name="update_question"),
    path("questions/<int:question_id>/delete/", delete_question, name="delete_question"),
    path('polls/<int:poll_id>/export/', export_poll_responses_csv, name='export_poll_responses'),
    path('', views.index, name='index'),
    path('join/', views.join_poll_view, name='join_poll'),
    path('<int:poll_id>/questions/', views.question_list, name='question_list'),

]