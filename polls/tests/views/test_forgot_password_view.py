from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ForgotPasswordViewTest(TestCase):
    def setUp(self):
        """Set up for forgot password page tests."""
        self.client = Client()
        self.forgot_password_url = reverse("forgot_password")

    def test_forgot_password_page_loads(self):
        """Test if the forgot password page loads successfully."""
        response = self.client.get(self.forgot_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Forgot Your Password?")  # Check if the text "Forgot Your Password?" exists in the HTML

    def test_forgot_password_with_valid_email(self):
        """Test if the password reset process works with a valid email."""
        # Create a user to test the reset functionality
        user = User.objects.create_user(username="existinguser", email="test@example.com", password="password123")
        response = self.client.post(self.forgot_password_url, {
            "email": "test@example.com",
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful password reset request
        # You might check for a redirect to the login page or a success message
        self.assertRedirects(response, reverse("login"))  # Assuming it redirects to the login page after a successful reset request

    def test_forgot_password_with_non_existent_email(self):
        """Test if the password reset fails when an email that doesn't exist is submitted."""
        response = self.client.post(self.forgot_password_url, {
            "email": "nonexistent@example.com",  # Email not in the database
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the forgot password page
        self.assertContains(response, "Email not found")  # Assuming an error message is shown for non-existent email

    def test_forgot_password_with_missing_email(self):
        """Test if the password reset fails when the email field is missing."""
        response = self.client.post(self.forgot_password_url, {
            "email": "",  # Missing email
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the forgot password page
        self.assertContains(response, "This field is required.")  # Check if the form validation error message is shown

    def test_forgot_password_button_text(self):
        """Test if the reset password button contains the correct text."""
        response = self.client.get(self.forgot_password_url)
        self.assertContains(response, "Reset Password")  # Check if the "Reset Password" text is in the button

    def test_back_button_functionality(self):
        """Test if the back button redirects correctly."""
        response = self.client.get(self.forgot_password_url)
        # Check if the back button redirects to the login page 
        self.assertContains(response, 'href="{% url \'login_interface\' %}"')  

    def test_forgot_password_redirect_after_successful_reset(self):
        """Test if the user is redirected after a successful reset request."""
        user = User.objects.create_user(username="existinguser", email="test@example.com", password="password123")
        response = self.client.post(self.forgot_password_url, {
            "email": "test@example.com",
        })
        self.assertRedirects(response, reverse("login"))  # Redirect to the login page after password reset
