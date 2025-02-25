import  csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def download_poll_responses(request, poll_id):
    poll=get_object_or_404(Poll, pk=poll_id)
    responses= Response.objects.filter(question_poll=poll).select_related('user', 'question', 'choice')

    response= HttpResponse(cotent_type='text/csv')
    response['Content-Disposition']= f'attachment; filename= "{poll.title}_responses.csv"'

    writer= csv.writer(response)
    writer= writerow('User', 'Question', 'Choice', 'Submitted At')

    for resp in responses:
        wri .writerow([resp.user.username, resp.question.question_text, resp.choice.choice_text, resp.submitted_at])

    return response