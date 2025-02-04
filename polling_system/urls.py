from django.contrib import admin
from django.urls import path, include
from polls import views

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Include all URLs from the polls app
    path('polls/', include('polls.urls')),

]