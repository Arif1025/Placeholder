from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Poll, Question, Choice, Response
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def homepage(request):
    return render(request, 'student_home_interface.html')

def index(request):
    return render(request, 'index.html')

#poll that a student sees
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = poll.questions.all().prefetch_related('choices')
    return render(request, 'poll_detail.html', {
        'poll': poll,
        'questions': questions
    })

@require_POST
#storing user response in table
def submit_response(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    
    responses = []
    for key, value in request.POST.items():
        if key.startswith("question_"):
            question_id = key.split("_")[1]
            choice_id = value
            
            try:
                question = Question.objects.get(pk=question_id, poll=poll)
                choice = Choice.objects.get(pk=choice_id, question=question)
                
                # Prevent duplicate responses
                existing_response = Response.objects.filter(user=request.user, question=question).exists()
                if existing_response:
                    return JsonResponse({'error': 'You have already submitted a response for this poll.'}, status=400)
                
                responses.append(Response(
                    user=request.user,
                    question=question,
                    choice=choice,
                    submitted_at=timezone.now()
                ))
            except (Question.DoesNotExist, Choice.DoesNotExist):
                return JsonResponse({'error': 'Invalid question or choice selection'}, status=400)

    Response.objects.bulk_create(responses)

    return JsonResponse({'status': 'success'})

#screen the teacher sees
def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = poll.questions.all().prefetch_related('choices')
    
    results = {}
    for question in questions:
        choices = question.choices.all()
        total_responses = Response.objects.filter(
            question=question
        ).count()
        
        results[question.id] = {
            'question_text': question.question_text,
            'total_responses': total_responses,
            'choices': {
                choice.id: {
                    'text': choice.choice_text,
                    'count': Response.objects.filter(choice=choice).count()
                } for choice in choices
            }
        }
    
    return render(request, 'poll_results.html', {
        'poll': poll,
        'results': results
    })