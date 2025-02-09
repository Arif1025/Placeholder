from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('polls/', views.poll_list, name='poll_list'),
    path('polls/create/', views.poll_create, name='poll_create'),
    path('polls/<int:poll_id>/edit/', views.poll_edit, name='poll_edit'),
    path('polls/<int:poll_id>/delete/', views.poll_delete, name='poll_delete'),
    path('polls/<int:poll_id>/questions/', views.question_list, name='question_list'),
    path('polls/<int:poll_id>/questions/create/', views.question_create, name='question_create'),
    path('polls/<int:poll_id>/questions/<int:question_id>/edit/', views.question_edit, name='question_edit'),
    path('polls/<int:poll_id>/questions/<int:question_id>/delete/', views.question_delete, name='question_delete'),
    path('polls/<int:poll_id>/questions/<int:question_id>/choices/', views.choice_list, name='choice_list'),
    path('polls/<int:poll_id>/questions/<int:question_id>/choices/create/', views.choice_create, name='choice_create'),
    path('polls/<int:poll_id>/questions/<int:question_id>/choices/<int:choice_id>/edit/', views.choice_edit, name='choice_edit'),
    path('polls/<int:poll_id>/questions/<int:question_id>/choices/<int:choice_id>/delete/', views.choice_delete, name='choice_delete'),
]