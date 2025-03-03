from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages

from .models import Poll

class JoinPollViewTests(TestCase):

    def setUp(self):
        """
        Create a user, a sample poll with a known code,
        and prepare a test client for making requests.
        """
        self.client = Client()

        self.teacher = User.objects.create_user(username='teacher', password='pass123')

        self.poll_with_code = Poll.objects.create(
            title="Sample Poll",
            description="Test poll with code",
            created_by=self.teacher,
            code="TEST123"
        )

    def test_join_poll_correct_code(self):
        """
        If the student enters a correct code (TEST123),
        they should be redirected to the question list for that poll.
        """
        url = reverse('join_poll')  
        response = self.client.post(url, {'code': 'TEST123'})

        expected_redirect = reverse('question_list', args=[self.poll_with_code.id])
        
        self.assertRedirects(response, expected_redirect)

    def test_join_poll_incorrect_code(self):
        """
        If the student enters an incorrect code,
        they should remain on the join page and see an error message.
        """
        url = reverse('join_poll')
        response = self.client.post(url, {'code': 'WRONG_CODE'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/join_poll.html')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("invalid" in str(m) for m in messages),
                        "Expected an error message containing 'invalid'")

    def test_join_poll_blank_code(self):
        """
        If the student enters no code, treat it as invalid.
        """
        url = reverse('join_poll')
        response = self.client.post(url, {'code': ''})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/join_poll.html')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("invalid" in str(m).lower() for m in messages),
                        "Expected an error message about an invalid code")

