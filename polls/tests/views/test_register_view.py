from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class RegisterViewTest(TestCase):
    def setUp(self):
        """Set up for registration page tests."""
        self.client = Client()
        self.register_url = reverse("register")  

    def test_register_page_loads(self):
        """Test if the registration page loads successfully."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create an Account")  

    def test_register_user_success(self):
        """Test if a user can register successfully."""
        response = self.client.post(self.register_url, {
            "username": "newuser",
            "password": "newpassword123",
            "role": "student",  
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username="newuser").exists())  

    def test_register_user_with_missing_field(self):
        """Test if the registration fails when a required field is missing."""
        response = self.client.post(self.register_url, {
            "username": "newuser", 
            "role": "teacher",
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "This field is required.")  

    def test_register_user_with_invalid_password(self):
        """Test if the registration fails with an invalid password (e.g., too short)."""
        response = self.client.post(self.register_url, {
            "username": "newuser",
            "password": "short", 
            "role": "student",
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "This password is too short.")  

    def test_register_user_duplicate_username(self):
        """Test if the registration fails when the username already exists."""
        # Create a user first
        User.objects.create_user(username="existinguser", password="password123")
        response = self.client.post(self.register_url, {
            "username": "existinguser", 
            "password": "newpassword123",
            "role": "teacher",
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "A user with that username already exists.")  

    def test_register_button_text(self):
        """Test if the registration button contains the correct text."""
        response = self.client.get(self.register_url)
        self.assertContains(response, "Register") 

    def test_back_button_functionality(self):
        """Test if the back button redirects correctly."""
        response = self.client.get(self.register_url)

        self.assertContains(response, 'href="index.html"')

    def test_register_user_redirect_after_registration(self):
        """Test if the user is redirected after a successful registration."""
        response = self.client.post(self.register_url, {
            "username": "newuser",
            "password": "newpassword123",
            "role": "student",
        })
        self.assertRedirects(response, reverse("login_interface/"))  
