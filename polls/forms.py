from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm
from .models import Question
from .models import Poll, Question, Choice

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
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        print("Cleaned title:", title)  # Log cleaned title
        if not title:
            raise forms.ValidationError("This field is required.")
        return title

    def clean_code(self):
        code = self.cleaned_data.get("code")
        if not code:
            raise forms.ValidationError("The code field is required.")
        return code
        
    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk:  # Only validate if poll exists (editing mode)
            question_count = Question.objects.filter(poll=self.instance).count()
            if question_count == 0:
                raise forms.ValidationError("A poll must have at least one question.")


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

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

QuestionFormSet = inlineformset_factory(Poll, Question, form=QuestionForm, extra=1, can_delete=True)
ChoiceFormSet = inlineformset_factory(Question, Choice, form=ChoiceForm, extra=3, can_delete=True)