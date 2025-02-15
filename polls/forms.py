from django import forms
from .models import Poll

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
    