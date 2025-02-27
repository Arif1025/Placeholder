from django.contrib import admin
from django.urls import path, include
from polls import views
from polls.views import register_teacher, login_teacher, logout_teacher

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('', views.homepage, name='home'),
    path("register/", register_teacher, name="register_teacher"),
    path("login/", login_teacher, name="login_teacher"),
    path("logout/", logout_teacher, name="logout_teacher"),
]