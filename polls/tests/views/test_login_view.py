from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class LoginViewTest(TestCase):
    def setUp(self):
        """Create a test user."""
        self.client = Client()
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse("login")  # Ensure your URL name is correct in urls.py
        self.forgot_password_url = reverse("forgot-password")  # Ensure your URL name for forgot-password page is correct
        self.register_url = reverse("register")  # Ensure your URL name for the register page is correct

    def test_login_page_loads(self):
        """Test if the login page loads successfully."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")  # Check if "Login" text is in the HTML

    def test_valid_login(self):
        """Test login with correct credentials."""
        response = self.client.post(self.login_url, {"username": self.username, "password": self.password})
        self.assertEqual(response.status_code, 302)  # Should redirect on successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_login(self):
        """Test login with incorrect credentials."""
        response = self.client.post(self.login_url, {"username": self.username, "password": "wrongpassword"})
        self.assertEqual(response.status_code, 200)  # Should reload the login page
        self.assertContains(response, "Invalid username or password")  # Adjust based on your template message
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_required_redirect(self):
        """Test if a protected page redirects to login."""
        protected_url = reverse("teacher_home_interface")  # Change this to any login-required view
        response = self.client.get(protected_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(self.login_url))  # Ensure redirect to login

    def test_logout(self):
        """Test if a logged-in user can log out successfully."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("logout"))  # Ensure your URL name is correct in urls.py
        self.assertEqual(response.status_code, 302)  # Should redirect on logout
        response = self.client.get(reverse("teacher_home_interface"))  # Test protected page after logout
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_forgot_password_link(self):
        """Test if the 'Forgot Password?' link exists on the login page and works."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Forgot Password?')  # Check if "Forgot Password?" link is present in the HTML
        self.assertContains(response, f'href="{self.forgot_password_url}"')  # Check if the link points to the correct URL

    def test_forgot_password_page(self):
        """Test if the forgot password page loads successfully."""
        response = self.client.get(self.forgot_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reset Password")

    def test_register_button_on_login_page(self):
        """Test if the 'Create an Account' button is present and links to the correct register page."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an Account')  # Check if "Create an Account" button is present in the HTML
        self.assertContains(response, f'href="{self.register_url}"')  # Check if the button links to the correct register URL
