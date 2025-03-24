from django.test import TestCase
from polling_system.models import Poll, Choice
from django.contrib.auth.models import User

class PollModeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')  # Create a test user
        self.poll = Poll.objects.create(question='what is your favourite subject?')  # Create a test poll

    def test_poll_creation(self):
        self.assertEqual(self.poll.question,'what is your favourite subject?')  # Test poll question
        self.assertEqual(self.poll.created_by.username, 'test')  # Test poll creator

    def test_vote_creation(self):
        vote=Choice.objects.create(poll=self.poll, user=self.user, choice='math')  # Create a test vote
        self.assertEqual(Choice.objects.count(), 1)  # Ensure one vote is created
        self.assertEqual(vote.choice, 'math')  # Check the vote choice is 'math'
