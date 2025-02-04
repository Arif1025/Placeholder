from django.shortcuts import render
import json
from .models import Poll, Response

def polling_results(request, poll_id):
    """
    View to display aggregated polling results for a specific poll.
    """
    # Retrieve poll object
    poll = Poll.objects.get(id=poll_id)

    # Get the questions for the poll
    questions = poll.questions.all()

    # Prepare data for the bar chart
    results = []
    for question in questions:
        # Get all choices and their response counts for the question
        choices = question.choices.all()
        choice_data = []
        for choice in choices:
            response_count = Response.objects.filter(question=question, choice=choice).count()
            choice_data.append({
                'choice_text': choice.choice_text,
                'response_count': response_count,
            })

        # Add question and its choice data to results
        results.append({
            'question_text': question.question_text,
            'choices': choice_data,
        })

    # Convert results to JSON for use in the template
    results_json = json.dumps(results)

    # Pass data to the template
    context = {
        'poll': poll,
        'results': results,
        'results_json': results_json,  # JSON version of results
    }
    return render(request, 'polls/polling_results.html', context)