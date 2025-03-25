from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from polls.models import Poll
from django.contrib.auth import get_user_model

User = get_user_model()

class JoinPollViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Teacher creates the poll
        self.teacher = User.objects.create_user(username='teacher', password='pass123', role='teacher')
        self.client.login(username='teacher', password='pass123')

        # Student logs in
        self.student = User.objects.create_user(username='student1', password='testpass', role='student')

        self.poll_with_code = Poll.objects.create(
            title="Sample Poll",
            description="Test poll with code",
            created_by=self.teacher,
            code="TEST123"
        )

    def test_join_poll_correct_code(self):
        self.client.login(username='student1', password='testpass')
        url = reverse('join_poll')
        response = self.client.post(url, {'poll_code': 'TEST123'})

        expected_redirect = reverse('student_home_interface')
        self.assertRedirects(response, expected_redirect)

    def test_join_poll_incorrect_code(self):
        url = reverse('join_poll')
        response = self.client.post(url, {'poll_code': 'WRONG_CODE'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enter_poll_code.html')

        form = response.context['form']
        self.assertFormError(form, 'poll_code', 'Invalid poll code.')


    def test_join_poll_blank_code(self):
        url = reverse('join_poll')
        response = self.client.post(url, {'poll_code': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enter_poll_code.html')


        # Check for default required error
        form = response.context['form']
        self.assertFormError(form, 'poll_code', 'This field is required.')
