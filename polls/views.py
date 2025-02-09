from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Poll, Question, Choice, Response
from .forms import PollForm, QuestionForm, ChoiceForm

def index(request):
    return HttpResponse("Hello, this is the index view.")

def homepage(request):
    return HttpResponse("Hello! This is the homepage at the root URL.")

@login_required
def poll_list(request):
    """List all polls."""
    polls = Poll.objects.all()
    return render(request, 'polls/poll_list.html', {'polls': polls})

@login_required
def poll_create(request):
    """Create a new poll."""
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.created_by = request.user 
            poll.save()
            return redirect('poll_list')
    else:
        form = PollForm()
    return render(request, 'polls/poll_form.html', {'form': form})

@login_required
def poll_edit(request, poll_id):
    """Edit an existing poll."""
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            return redirect('poll_list')
    else:
        form = PollForm(instance=poll)
    return render(request, 'polls/poll_form.html', {'form': form, 'poll': poll})

@login_required
def poll_delete(request, poll_id):
    """Delete a poll."""
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == 'POST':
        poll.delete()
        return redirect('poll_list')
    return render(request, 'polls/poll_confirm_delete.html', {'poll': poll})

@login_required
def question_list(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    questions = poll.questions.all()  
    return render(request, 'polls/question_list.html', {
        'poll': poll,
        'questions': questions
    })

@login_required
def question_create(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.poll = poll
            question.save()
            return redirect('question_list', poll_id=poll.id)
    else:
        form = QuestionForm()
    return render(request, 'polls/question_form.html', {'form': form, 'poll': poll})

@login_required
def question_edit(request, poll_id, question_id):
    question = get_object_or_404(Question, id=question_id, poll__id=poll_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_list', poll_id=poll_id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'polls/question_form.html', {'form': form, 'question': question})

@login_required
def question_delete(request, poll_id, question_id):
    question = get_object_or_404(Question, id=question_id, poll__id=poll_id)
    if request.method == 'POST':
        question.delete()
        return redirect('question_list', poll_id=poll_id)
    return render(request, 'polls/question_confirm_delete.html', {'question': question})

@login_required
def choice_list(request, poll_id, question_id):
    question = get_object_or_404(Question, id=question_id, poll__id=poll_id)
    choices = question.choices.all()  
    return render(request, 'polls/choice_list.html', {
        'question': question,
        'choices': choices
    })

@login_required
def choice_create(request, poll_id, question_id):
    question = get_object_or_404(Question, id=question_id, poll__id=poll_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('choice_list', poll_id=poll_id, question_id=question_id)
    else:
        form = ChoiceForm()
    return render(request, 'polls/choice_form.html', {'form': form, 'question': question})

@login_required
def choice_edit(request, poll_id, question_id, choice_id):
    choice = get_object_or_404(Choice, id=choice_id, question__id=question_id, question__poll__id=poll_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            return redirect('choice_list', poll_id=poll_id, question_id=question_id)
    else:
        form = ChoiceForm(instance=choice)
    return render(request, 'polls/choice_form.html', {'form': form, 'choice': choice})

@login_required
def choice_delete(request, poll_id, question_id, choice_id):
    choice = get_object_or_404(Choice, id=choice_id, question__id=question_id, question__poll__id=poll_id)
    if request.method == 'POST':
        choice.delete()
        return redirect('choice_list', poll_id=poll_id, question_id=question_id)
    return render(request, 'polls/choice_confirm_delete.html', {'choice': choice})
