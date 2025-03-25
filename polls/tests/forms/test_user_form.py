from django.test import TestCase
from polls.forms import CustomUserCreationForm, CustomLoginForm
from polls.models import CustomUser


class CustomUserCreationFormTests(TestCase):
    def test_valid_form_creates_user(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'role': 'student',
            'password1': 'Testpass123',
            'password2': 'Testpass123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'student')


    def test_missing_fields(self):
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('role', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

    def test_password_too_short(self):
        form_data = {
            'username': 'shortpassuser',
            'email': 'short@example.com',
            'role': 'teacher',
            'password1': '123',
            'password2': '123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_duplicate_username_fails(self):
        CustomUser.objects.create_user(username='existing', password='Testpass123', role='student')
        form_data = {
            'username': 'existing',
            'password': 'Testpass123',
            'role': 'student'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class CustomLoginFormTests(TestCase):
    def test_form_fields_exist(self):
        form = CustomLoginForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        self.assertIn('role', form.fields)

    def test_valid_login_data(self):
        form_data = {
            'username': 'myuser',
            'password': 'mypassword',
            'role': 'teacher',
        }
        form = CustomLoginForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Login form should be valid, got errors: {form.errors}")

    def test_login_form_missing_fields(self):
        form = CustomLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)
        self.assertIn('role', form.errors)
