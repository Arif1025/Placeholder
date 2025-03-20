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
        self.assertContains(response, "Forgot Your Password")  

    def test_forgot_password_with_valid_username(self):
        """Test if the password reset process works with a valid username."""
        # Create a user to test the reset functionality
        user = User.objects.create_user(username="existinguser", email="test@example.com", password="password123")
        response = self.client.post(self.forgot_password_url, {
            "username": "existinguser",  
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful password reset request

        self.assertRedirects(response, reverse("login"))  # Redirects to the login page after a successful reset request

    def test_forgot_password_with_non_existent_username(self):
        """Test if the password reset fails when a username that doesn't exist is submitted."""
        response = self.client.post(self.forgot_password_url, {
            "username": "nonexistentuser",  # Username not in the database
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the forgot password page
        self.assertContains(response, "Username not found")  # Assuming an error message is shown for non-existent username

    def test_forgot_password_with_missing_username(self):
        """Test if the password reset fails when the username field is missing."""
        response = self.client.post(self.forgot_password_url, {
            "username": "",  # Missing username
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the forgot password page
        self.assertContains(response, "This field is required.")  # Check if the form validation error message is shown

    def test_forgot_password_with_valid_new_password(self):
        """Test if a new password and confirm password work correctly."""
        user = User.objects.create_user(username="existinguser", email="test@example.com", password="password123")
        response = self.client.post(self.forgot_password_url, {
            "username": "existinguser",
            "new_password": "newpassword123",  # New password
            "confirm_password": "newpassword123",  # Confirm password matches new password
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful password reset
        self.assertRedirects(response, reverse("login"))  # Redirects to the login page after a successful reset request

    def test_forgot_password_with_mismatched_passwords(self):
        """Test if mismatched passwords are handled correctly."""
        user = User.objects.create_user(username="existinguser", email="test@example.com", password="password123")
        response = self.client.post(self.forgot_password_url, {
            "username": "existinguser",
            "new_password": "newpassword123",  # New password
            "confirm_password": "differentpassword123",  # Confirm password does not match
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the forgot password page
        self.assertContains(response, "The two password fields didn’t match.")  # Check if the error message for mismatched passwords appears

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
            "username": "existinguser",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123",
        })
        self.assertRedirects(response, reverse("login"))  # Redirect to the login page after password reset
