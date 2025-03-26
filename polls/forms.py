from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Question
from .models import Poll, Question, Choice, CustomUser

# Custom Login Form for authentication with role selection (Student or Teacher)
class CustomLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    role = forms.ChoiceField(choices=[('student', 'Student'), ('teacher', 'Teacher')], required=True, label="Login as")
    

# Custom User Creation Form to handle user registration with email, username, and role
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"id": "email"}))  # Email input field with custom ID
    username = forms.CharField(widget=forms.TextInput(attrs={"id": "username"}))  # Username input field with custom ID
    role = forms.ChoiceField(
        choices=[('student', 'Student'), ('teacher', 'Teacher')],  # Role choices for the user
        widget=forms.Select(attrs={"id": "role"}),  # Custom widget for role field
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "role", "password1", "password2"]  # include both password fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user

# Poll creation form to define a new poll with a title, description, code, and completion status
class PollForm(forms.ModelForm):
    class Meta:
        model = Poll  # The model associated with the form
        fields = ['title', 'description', 'code']  # Fields for the form

    def clean_title(self):
        # Title field validation: it should not be empty
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("This field is required.")
        return title

    def clean_code(self):
        # Code field validation: it should not be empty
        code = self.cleaned_data.get("code")
        if not code:
            raise forms.ValidationError("The code field is required.")
        return code

    def clean(self):
        # Custom validation to ensure a poll has at least one question
        cleaned_data = super().clean()
        if self.instance.pk:
            question_count = Question.objects.filter(poll=self.instance).count()
            if question_count == 0:
                raise forms.ValidationError("A poll must have at least one question.")
        return cleaned_data

# Form to join an existing poll by providing its code
class JoinPollForm(forms.Form):
    poll_code = forms.CharField(max_length=20, label="Poll Code")  # Field for entering poll code

    def clean_poll_code(self):
        # Validation to check if the poll code exists in the database
        code = self.cleaned_data.get('poll_code')
        try:
            poll = Poll.objects.get(code=code)
        except Poll.DoesNotExist:
            raise forms.ValidationError('Invalid poll code.')  # Error if poll code is invalid
        return code

# Form to create or edit a Question for a poll
class QuestionForm(forms.ModelForm):
    options = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text="Enter one option per line."
    )

    class Meta:
        model = Question
        fields = ['text', 'question_type', 'correct_answer']

    text = forms.CharField(label="Question Text", widget=forms.Textarea)  # Text field for question
    question_type = forms.ChoiceField(choices=[('written', 'Written Answer'), ('mcq', 'Multiple Choice')])  # Question type field
    options = forms.CharField(widget=forms.Textarea, required=False, help_text="Enter one option per line.")  # Options for MCQ

# Form for creating or editing a Choice for a question
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice  # The model associated with the form
        fields = ['text']  # Field for choice text

# Formset for managing multiple questions in a poll (inline formset)
QuestionFormSet = inlineformset_factory(Poll, Question, form=QuestionForm, extra=1, can_delete=True)  # Poll to Question relation
ChoiceFormSet = inlineformset_factory(Question, Choice, form=ChoiceForm, extra=3, can_delete=True)  # Question to Choice relation

# Form for submitting answers to questions in a poll
class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)  # Get the question instance passed to the form
        super().__init__(*args, **kwargs)

        # Conditional rendering based on question type (MCQ or written answer)
        if question.question_type == 'mcq':
            choices = [(choice.id, choice.text) for choice in question.choices.all()]  # MCQ choices
            self.fields['answer'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,  # Radio button for MCQs
                label=question.text  # Label with the question text
            )
        else:
            self.fields['answer'] = forms.CharField(
                widget=forms.Textarea,  # Textarea for written answers
                label=question.text,  # Label with the question text
                required=True  # Make this field required
            )
            