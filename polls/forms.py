from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Question
from .models import Poll, Question, Choice, CustomUser

class CustomLoginForm(AuthenticationForm):
    role = forms.ChoiceField(
        choices=[('student', 'Student'), ('teacher', 'Teacher')],
        required=True,
        label="Login as"
    )
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"id": "email"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"id": "username"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password"}))
    role = forms.ChoiceField(
    choices=[('student', 'Student'), ('professor', 'Teacher')],
    widget=forms.Select(attrs={"id": "role"}),
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "role", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user
    
class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description', 'code', 'is_done'] 

    def clean_title(self):
        title = self.cleaned_data.get('title')
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
        if self.instance.pk:
            question_count = Question.objects.filter(poll=self.instance).count()
            if question_count == 0:
                raise forms.ValidationError("A poll must have at least one question.")
        return cleaned_data


class JoinPollForm(forms.Form):
    poll_code = forms.CharField(max_length=20, label="Poll Code")

    def clean_poll_code(self):
        code = self.cleaned_data.get('poll_code')
        try:
            poll = Poll.objects.get(code=code)
        except Poll.DoesNotExist:
            raise forms.ValidationError('Invalid poll code.')
        return code
    

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

class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

        if question.question_type == 'mcq':
            choices = [(choice.id, choice.choice_text) for choice in question.choices.all()]
            self.fields['answer'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label=question.text
            )
        else:
            self.fields['answer'] = forms.CharField(
                widget=forms.Textarea,
                label=question.text,
                required=True
            )