from django.test import TestCase
from polling_system.models import Poll, Choice
from django.contrib.auth.models import User

class PollModeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.poll = Poll.objects.create(question='what is your favourite subject?')

    def test_poll_creation(self):
        self.assertEqual(self.poll.question,'what is your favourite subject?')
        self.assertEqual(self.poll.created_by.username, 'test')

    def test_vote_creation(self):
        vote=Choice.objects.create(poll=self.poll, user=self.user, choice='math')
        self.assertEqual(Choice.objects.count(), 1)
        self.assertEqual(vote.choice, 'math')