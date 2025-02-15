from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('join/', views.join_poll_view, name='join_poll'),
    path('<int:poll_id>/questions/', views.question_list, name='question_list'),

]