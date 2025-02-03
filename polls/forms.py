from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    role = forms.ChoiceField(
        choices=[('student', 'Student'), ('professor', 'Professor')],
        required=True,
        label="Login as"
    )