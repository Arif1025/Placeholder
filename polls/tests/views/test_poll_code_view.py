from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from polls.models import Poll

User = get_user_model()


class EnterPollCodeViewTest(TestCase):
    """Tests for the enter_poll_code view where students join polls via code."""

    def setUp(self):
        self.student = User.objects.create_user(username='student1', password='Password123', role='student')
        self.poll = Poll.objects.create(
            title='Test Poll',
            description='A sample poll',
            created_by=self.student,
            code='JOIN123'
        )
        self.url = reverse('enter_poll_code')

    def test_redirects_anonymous_user_to_login(self):
        """Anonymous users should be redirected to login."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login_interface"), response.url)

    def test_logged_in_student_can_view_poll_code_page(self):
        """Student can load the poll code entry page."""
        self.client.login(username='student1', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enter_poll_code.html')
        self.assertContains(response, "Poll Code")

    def test_valid_poll_code_adds_student_to_poll(self):
        """Submitting a valid poll code adds the user as a participant and redirects home."""
        self.client.login(username='student1', password='Password123')
        response = self.client.post(self.url, {'poll_code': 'JOIN123'})
        self.assertRedirects(response, reverse("student_home_interface"))
        self.poll.refresh_from_db()
        self.assertIn(self.student, self.poll.participants.all())

    def test_invalid_poll_code_does_not_join(self):
        """Invalid code should not add the student or redirect."""
        self.client.login(username='student1', password='Password123')
        response = self.client.post(self.url, {'poll_code': 'WRONGCODE'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid poll code')
        self.assertNotIn(self.student, self.poll.participants.all())

    def test_empty_poll_code_shows_form_error(self):
        """Submitting empty poll code shows validation error."""
        self.client.login(username='student1', password='Password123')
        response = self.client.post(self.url, {'poll_code': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')


class EndPollViewTest(TestCase):
    """Tests for the end_poll view, which ends an active poll."""

    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="password123", role="teacher")
        self.student = User.objects.create_user(username="student", password="password123", role="student")
        self.poll = Poll.objects.create(
            title="Poll to End",
            created_by=self.teacher,
            code="END123",
            is_done=False
        )
        self.url = reverse('end_poll', args=[self.poll.id])

    def test_teacher_can_end_poll_successfully(self):
        """Teacher should be able to end poll (set is_done=True, code=None)."""
        self.client.login(username="teacher", password="password123")
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("teacher_home_interface"))
        self.poll.refresh_from_db()
        self.assertTrue(self.poll.is_done)
        self.assertIsNone(self.poll.code)

    def test_student_cannot_end_poll(self):
        """Students should not be able to end a poll."""
        self.client.login(username="student", password="password123")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_get_request_does_not_end_poll(self):
        """GET request should not change poll status."""
        self.client.login(username="teacher", password="password123")
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("teacher_home_interface"))
        self.poll.refresh_from_db()
        self.assertFalse(self.poll.is_done)
        self.assertIsNotNone(self.poll.code)
