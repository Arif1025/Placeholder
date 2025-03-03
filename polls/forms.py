from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Question
from .models import Poll

class CustomLoginForm(AuthenticationForm):
    role = forms.ChoiceField(
        choices=[('student', 'Student'), ('professor', 'Professor')],
        required=True,
        label="Login as"
    )

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description', 'code'] 


class JoinPollForm(forms.Form):
    code = forms.CharField(max_length=20, label="Enter Poll Code")

    def clean_code(self):
        data = self.cleaned_data['code'].strip()
        if not data:
            raise forms.ValidationError("The code you have entered is invalid.")
        return data
    

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'options']

    OPTIONS_HELP_TEXT = "For multiple-choice questions, separate options with a comma."

    text = forms.CharField(label="Question Text", widget=forms.Textarea)
    question_type = forms.ChoiceField(choices=[('text', 'Written Answer'), ('mcq', 'Multiple Choice')])
    options = forms.CharField(required=False, help_text=OPTIONS_HELP_TEXT)
