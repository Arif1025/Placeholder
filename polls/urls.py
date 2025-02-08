from django.urls import path
from .views import *

urlpatterns = [
    path("polls/", poll_list, name="poll_list"),
    path("polls/create/", create_poll, name="create_poll"),
    path("polls/<int:poll_id>/update/", update_poll, name="update_poll"),
    path("polls/<int:poll_id>/delete/", delete_poll, name="delete_poll"),

    path("polls/<int:poll_id>/questions/", question_list, name="question_list"),
    path("polls/<int:poll_id>/questions/create/", create_question, name="create_question"),
    path("questions/<int:question_id>/update/", update_question, name="update_question"),
    path("questions/<int:question_id>/delete/", delete_question, name="delete_question"),
]