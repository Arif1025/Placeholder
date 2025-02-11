from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('<int:poll_id>/submit/', views.submit_response, name='submit_response'),
    path('<int:poll_id>/results/', views.poll_results, name='poll_results'),
]