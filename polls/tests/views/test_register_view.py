from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterViewTest(TestCase):
    def setUp(self):
        self.register_url = reverse("register")

    def test_register_page_loads(self):
        """Page loads successfully with form and text."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create an Account")
        self.assertContains(response, "Register")

    def test_register_user_success_as_student(self):
        """Register a new student successfully with matching passwords and valid email."""
        response = self.client.post(self.register_url, {
            "username": "newstudent",
            "password": "newpassword123",
            "confirm_password": "newpassword123",
            "role": "student"
        })
        self.assertRedirects(response, reverse("student_home_interface"))
        self.assertTrue(User.objects.filter(username="newstudent").exists())

    def test_register_user_success_as_teacher(self):
        """Register a teacher account and redirect to correct dashboard."""
        response = self.client.post(self.register_url, {
            "username": "newteacher",
            "password": "newpassword123",
            "confirm_password": "newpassword123",
            "role": "teacher"
        })
        self.assertRedirects(response, reverse("teacher_home_interface"))
        self.assertTrue(User.objects.filter(username="newteacher", role="teacher").exists())

    def test_register_missing_fields(self):
        """Missing required fields should return validation error."""
        response = self.client.post(self.register_url, {
            "username": "",
            "password": "",
            "confirm_password": "",
            "role": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All fields are required.")

    def test_register_passwords_do_not_match(self):
        """Form rejects if password1 != password2."""
        response = self.client.post(self.register_url, {
            "username": "user1",
            "password": "password123",
            "confirm_password": "different123",
            "role": "student"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match!")

    def test_register_password_too_short(self):
        response = self.client.post(self.register_url, {
            "username": "user2",
            "password": "short1",
            "confirm_password": "short1",
            "role": "student"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password must be at least 8 characters long")

    def test_register_password_requires_digit(self):
        response = self.client.post(self.register_url, {
            "username": "user3",
            "password": "longpassword",
            "confirm_password": "longpassword",
            "role": "student"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password must contain at least one number.")

    def test_register_duplicate_username_fails(self):
        User.objects.create_user(username="existinguser", password="password123")
        response = self.client.post(self.register_url, {
            "username": "existinguser",
            "password": "anotherpass123",
            "confirm_password": "anotherpass123",
            "role": "teacher"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username already taken!")

    def test_register_back_button_exists(self):
        response = self.client.get(self.register_url)
        self.assertContains(response, "Back")

    def test_register_button_text_and_fields(self):
        response = self.client.get(self.register_url)
        self.assertContains(response, '<button type="submit"', html=False)
        self.assertContains(response, "Register")
        self.assertContains(response, "Username")
        self.assertContains(response, "Password")
        self.assertContains(response, "Role")
