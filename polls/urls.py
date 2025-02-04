from django.urls import path
from . import views

urlpatterns = [

    path('results/<int:poll_id>/', views.polling_results, name='polling_results'),
]