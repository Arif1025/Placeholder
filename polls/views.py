from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import JoinPollForm
from .models import Poll

def index(request):
    return HttpResponse("Hello, this is the index view.")

def homepage(request):
    return HttpResponse("Hello! This is the homepage at the root URL.")

def join_poll_view(request):
    if request.method == 'POST':
        form = JoinPollForm(request.POST)
        if form.is_valid():
            code_entered = form.cleaned_data['code']
            try:
                poll = Poll.objects.get(code=code_entered)
                return redirect('question_list', poll_id=poll.id)
            except Poll.DoesNotExist:
                messages.error(request, "The code you have entered is invalid.")
    else:
        form = JoinPollForm()
    
    return render(request, 'polls/join_poll.html', {'form': form})