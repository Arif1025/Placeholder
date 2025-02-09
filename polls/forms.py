from django import forms
from .models import Poll, Question, Choice

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description']
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['poll', 'question_text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'choice_text']
