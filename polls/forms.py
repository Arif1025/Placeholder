from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Poll, Question

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class TeacherRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class TeacherLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomLoginForm(AuthenticationForm):
    role = forms.ChoiceField(
        choices=[('student', 'Student'), ('professor', 'Professor')],
        required=True,
        label="Login as"
    )
    
