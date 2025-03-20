from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from polls.models import Poll

User = get_user_model()

class EnterPollCodeViewTest(TestCase):
    """Tests for the Enter Poll Code page (enter_poll_code view)."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('enter_poll_code')
        self.user = User.objects.get(username='@johndoe')

    def test_enter_poll_code_url(self):
        """Ensure the URL path for 'enter_poll_code' is what we expect."""
        self.assertEqual(self.url, '/enter_poll_code/')

    def test_get_enter_poll_code_anonymous(self):
        """Unauthenticated users can still view the code entry page (assuming no login required)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enter_poll_code.html')
        self.assertContains(response, '<h1>Poll Code</h1>')
        self.assertContains(response, "Please enter the code of the poll you'd like to join.")
        self.assertContains(response, '<input type="text" id="pollCode" name="pollCode" placeholder="Poll Code" required>')
        self.assertContains(response, '<button type="submit" class="join-button">Join</button>')
        self.assertContains(response, '<a href="javascript:history.back()" class="back-button">Back</a>')
        self.assertContains(response, '<button class="logout-button">Logout</button>')

    def test_get_enter_poll_code_logged_in(self):
        """A logged-in user can access the poll code entry page, sees the same content."""
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enter_poll_code.html')

    def test_submit_poll_code_form_valid(self):
        """
        Submitting a valid code should redirect the user 
        to the question_template (or wherever your code says).
        """
        response = self.client.post(self.url, {'pollCode': '12345'})
        self.assertRedirects(response, '/question_template/')  # or use reverse('question_template')

    def test_submit_poll_code_form_empty(self):
        """Submitting an empty poll code should re-render form with a validation error."""
        response = self.client.post(self.url, {'pollCode': ''})
        # Ensure the view or form signals an error
        # If you have a form, you might do: self.assertFormError(response, 'form', 'pollCode', 'This field is required.')
        # Or if you manually handle it, check for an error message:
        self.assertContains(response, 'Invalid poll code')

class EndPollViewTest(TestCase):
    """Tests for the 'end_poll' view that ends a poll (sets is_done=True, code=None)."""

    def setUp(self):
        self.teacher_user = User.objects.create_user(username="teacher", password="password123")
        self.student_user = User.objects.create_user(username="student", password="password123")

        # Log in teacher by default
        self.client.login(username="teacher", password="password123")

        # Create an active poll
        self.poll = Poll.objects.create(
            title="Active Poll",
            description="Not done yet",
            created_by=self.teacher_user,
            code="TEST123",
            is_done=False
        )
        self.end_poll_url = reverse('end_poll', args=[self.poll.id])

    def test_end_poll_success(self):
        """
        A teacher (creator) can successfully end the poll: sets poll.is_done=True and poll.code=None,
        then redirects to the teacher home page.
        """
        response = self.client.post(self.end_poll_url)
        self.assertRedirects(response, "/teacher_home_interface/")

        self.poll.refresh_from_db()
        self.assertTrue(self.poll.is_done, "Poll should be ended.")
      
