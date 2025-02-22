from django.test import TestCase
from django.contrib.auth.models import User
from polls.forms import CustomLoginForm  # Adjust import if your form is in a different location

class CustomLoginFormTest(TestCase):
    def setUp(self):
        """Create a test user."""
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_valid_form(self):
        """Test the login form with valid data."""
        form_data = {"username": self.username, "password": self.password}
        form = CustomLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_username(self):
        """Test the login form with missing username."""
        form_data = {"username": "", "password": self.password}
        form = CustomLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_invalid_form_missing_password(self):
        """Test the login form with missing password."""
        form_data = {"username": self.username, "password": ""}
        form = CustomLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_invalid_form_blank_data(self):
        """Test the login form with completely blank data."""
        form_data = {"username": "", "password": ""}
        form = CustomLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)