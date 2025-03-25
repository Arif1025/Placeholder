# polls/tests/views/test_forgot_password_view.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ForgotPasswordViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="existinguser", email="test@example.com", password="oldpassword123", role="student")
        self.forgot_password_url = reverse("forgot_password")
        self.reset_password_url = reverse("reset_password")

    def test_forgot_password_page_loads(self):
        response = self.client.get(self.forgot_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Forgot Your Password")

    def test_forgot_password_valid_username_sets_session(self):
        response = self.client.post(self.forgot_password_url, {"username": "existinguser"})
        session = self.client.session
        self.assertEqual(session.get("reset_username"), "existinguser")
        self.assertRedirects(response, self.reset_password_url)

    def test_forgot_password_invalid_username_stays_on_page(self):
        response = self.client.post(self.forgot_password_url, {"username": "fakeuser"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No account found with this username.")

    def test_reset_password_page_requires_session(self):
        response = self.client.get(self.reset_password_url)
        self.assertRedirects(response, self.forgot_password_url)

    def test_reset_password_successful_update(self):
        # Set session manually
        session = self.client.session
        session["reset_username"] = "existinguser"
        session.save()

        response = self.client.post(self.reset_password_url, {
            "password1": "Newpass123",
            "password2": "Newpass123",
        })
        self.assertRedirects(response, reverse("login_interface"))
        user = User.objects.get(username="existinguser")
        self.assertTrue(user.check_password("Newpass123"))

    def test_reset_password_passwords_do_not_match(self):
        session = self.client.session
        session["reset_username"] = "existinguser"
        session.save()

        response = self.client.post(self.reset_password_url, {
            "password1": "Newpass123",
            "password2": "Wrongpass",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match.")

    def test_reset_password_too_short(self):
        session = self.client.session
        session["reset_username"] = "existinguser"
        session.save()

        response = self.client.post(self.reset_password_url, {
            "password1": "short",
            "password2": "short",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password must be at least 8 characters long.")

    def test_reset_password_requires_digit(self):
        session = self.client.session
        session["reset_username"] = "existinguser"
        session.save()

        response = self.client.post(self.reset_password_url, {
            "password1": "passwordonly",
            "password2": "passwordonly",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password must contain at least one number.")

    def test_reset_password_session_expires(self):
        session = self.client.session
        session["reset_username"] = ""
        session.save()

        response = self.client.get(self.reset_password_url)
        self.assertRedirects(response, self.forgot_password_url)

    def test_reset_password_button_and_back_link(self):
        response = self.client.get(self.forgot_password_url)
        self.assertContains(response, "Reset Password")
        self.assertContains(response, reverse("login_interface"))
