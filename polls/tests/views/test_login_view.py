from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginViewTest(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.login_url = reverse("login_interface")
        self.logout_url = reverse("logout")
        self.forgot_password_url = reverse("forgot_password")
        self.register_url = reverse("register")
        self.teacher = User.objects.create_user(username="teacher1", password=self.password, role="teacher")
        self.student = User.objects.create_user(username="student1", password=self.password, role="student")

    def test_login_page_loads_successfully(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertTemplateUsed(response, "login_interface.html")

    def test_valid_login_redirects_teacher(self):
        response = self.client.post(self.login_url, {
            "username": "teacher1",
            "password": self.password,
            "role": "teacher"
        })
        self.assertRedirects(response, reverse("teacher_home_interface"))

    def test_valid_login_redirects_student(self):
        response = self.client.post(self.login_url, {
            "username": "student1",
            "password": self.password,
            "role": "student"
        })
        self.assertRedirects(response, reverse("student_home_interface"))

    def test_invalid_login_credentials(self):
        response = self.client.post(self.login_url, {
            "username": self.username,
            "password": "wrongpass",
            "role": "student"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_missing_credentials_shows_error(self):
        response = self.client.post(self.login_url, {
            "username": "",
            "password": "",
            "role": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_login_form_contains_role_field(self):
        response = self.client.get(self.login_url)
        self.assertContains(response, "Login as")
        self.assertContains(response, '<select name="role"')

    def test_protected_teacher_view_requires_login(self):
        protected_url = reverse("teacher_home_interface")
        response = self.client.get(protected_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.login_url, response.url)

    def test_logout_redirects_to_login(self):
        self.client.login(username="teacher1", password=self.password)
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)

    def test_forgot_password_link_visible(self):
        response = self.client.get(self.login_url)
        self.assertContains(response, "Forgot Password?")
        self.assertContains(response, f'href="{self.forgot_password_url}"')

    def test_register_link_visible(self):
        response = self.client.get(self.login_url)
        self.assertContains(response, "Create an Account")
        self.assertContains(response, f'href="{self.register_url}"')
