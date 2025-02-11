from django.test import TestCase, Client
from django.urls import reverse
from .models import Poll, Question, Choice, Response
from django.contrib.auth.models import User

class ResponseHandlingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.poll = Poll.objects.create(
            title="Test Math Quiz",
            description="A quiz for testing",
            created_by=self.user
        )
        
        self.question = Question.objects.create(
            poll=self.poll,
            question_text="What is 2+2?"
        )
        
        self.choice1 = Choice.objects.create(
            question=self.question,
            choice_text="4"
        )
        
        self.choice2 = Choice.objects.create(
            question=self.question,
            choice_text="5"
        )

        self.client = Client()

    def test_can_view_poll(self):
        response = self.client.get(reverse('poll_detail', args=[self.poll.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Math Quiz")
        self.assertContains(response, "What is 2+2?")
        self.assertContains(response, "4")
        self.assertContains(response, "5")

    def test_can_submit_response(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Changed to match the view's expected format
        response = self.client.post(
            reverse('submit_response', args=[self.poll.id]),
            {
                f'question_{self.question.id}': self.choice1.id
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'success'}
        )

        self.assertTrue(
            Response.objects.filter(
                question=self.question,
                choice=self.choice1,
                user=self.user
            ).exists()
        )

    def test_cannot_submit_invalid_choice(self):
        # Changed to match the view's expected format
        response = self.client.post(
            reverse('submit_response', args=[self.poll.id]),
            {
                f'question_{self.question.id}': 9999
            }
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'Invalid question or choice selection'}
        )

    def test_poll_results_calculation(self):
        Response.objects.create(
            question=self.question,
            choice=self.choice1,
            user=self.user
        )
        Response.objects.create(
            question=self.question,
            choice=self.choice1
        )
        Response.objects.create(
            question=self.question,
            choice=self.choice2
        )

        response = self.client.get(reverse('poll_results', args=[self.poll.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2 responses")
        self.assertContains(response, "1 responses")