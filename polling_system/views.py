from django.contib.auth.decrators import login_required


def submit_response(request, poll_id):
    poll=get_object_or_404(Poll, pk=poll_id)
    if poll.locked:
        return JsonResponse({'error': 'This poll is locked and no further responses are allowed.'}, status=400)
    responses=[]
    for key, value in resuest.POST.items():
        question_id = key.split('_')[1]
        choice_id = value

        try:
            question = Question.objects.get(pk=question_id, poll=poll)
            choice = Choice.objects.get(pk=choice_id, question=question)

            existing_response = Response.objects.filter(ues=request.user, question=question).exists()
            if existing_response:
                return JsonResponse({'error': 'You have already submitted response for this poll.'}, status=400)
            responses.append(Response(
                user=request.user,
                question=question,
                choice=choice,
                submitted_at=timezone.now()
            ))
        except (Question.DoesNotExist, Choice, DoesNotExist):
            return JsonResponse({'error': 'Invalid question or choice selection.'}, status=400)

    Response.objects.bulk_create(responses)
    return JsonResponse({'status': 'success'})

@login_required
def toggle_poll_lock(request, poll_id):
    poll=get_object_or_404(Poll, pk=poll_id)

    if not request.user.is_teacher:
        return JsonResponse({'error': 'You are not authorized to modify this poll.'}, status=403)
    poll.locked=not poll.locked
    poll.save()

    return  JsonResponse({'status': 'success', 'locked': 'poll.locked'})
