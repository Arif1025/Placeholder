from django.test import TestCase
from django.urls import reverse
from tutorials.models import User

class EnterPollCodeViewTestCase(TestCase):
    """Tests for the Enter Poll Code page."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('enter_poll_code') 
        self.user = User.objects.get(username='@johndoe')

    def test_enter_poll_code_url(self):
        """Test that the URL is correct."""
        self.assertEqual(self.url, '/enter_poll_code/')  

    def test_get_enter_poll_code(self):
        """Test that the Enter Poll Code page loads properly."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enter_poll_code.html')

        # Check for expected elements in the HTML (e.g., title, welcome message, input box, and button)
        self.assertContains(response, '<h1>Poll Code</h1>')
        self.assertContains(response, 'Please enter the code of the poll you\'d like to join.')
        self.assertContains(response, '<input type="text" id="pollCode" name="pollCode" placeholder="Poll Code" required>')
        self.assertContains(response, '<button type="submit" class="join-button">Join</button>')

        # Check for the back button's presence
        self.assertContains(response, '<a href="javascript:history.back()" class="back-button">Back</a>')

    def test_get_enter_poll_code_logged_in(self):
        """Test that logged-in users can access the Enter Poll Code page."""
        self.client.login(username=self.user.username, password="Password123")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enter_poll_code.html')

    def test_logout_button(self):
        """Test that the 'Logout' button is visible on the Enter Poll Code page."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="logout-button">Logout</button>')

    def test_submit_poll_code_form(self):
        """Test that the form can be submitted (and it redirects to question_template.html)."""
        # Simulate submitting a valid poll code
        response = self.client.post(self.url, {'pollCode': '12345'})

        # After submission, it should redirect to question_template.html
        self.assertRedirects(response, '/question_template/')  

    def test_poll_code_input_field(self):
        """Test that the input field is present and required."""
        response = self.client.get(self.url)
        self.assertContains(response, 'required')  # Ensure the input field is required

    def test_poll_code_input_validation(self):
        """Test that an invalid form submission (empty poll code) is not accepted."""
        response = self.client.post(self.url, {'pollCode': ''})
        
        # Check that the form is not valid (should show a validation error)
        self.assertFormError(response, 'form', 'pollCode', 'This field is required.')
