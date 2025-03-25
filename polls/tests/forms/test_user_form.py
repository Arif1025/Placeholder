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
            'password2': 'Testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'student')

    def test_password_mismatch_fails(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'role': 'teacher',
            'password1': 'Testpass123',
            'password2': 'Wrongpass'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_duplicate_email_fails(self):
        # Pre-create user
        CustomUser.objects.create_user(username='existinguser', email='test@example.com', password='pass123', role='student')

        form_data = {
            'username': 'newuser',
            'email': 'test@example.com',  # Duplicate email
            'role': 'teacher',
            'password1': 'Testpass123',
            'password2': 'Testpass123'
        }
        form = CustomUserCreationForm(data=form_data)

        form.is_valid()  # This populates form.errors

        # Just print for debugging if needed
        print("Errors:", form.errors)

        # Only check if you actually validate email uniqueness in your form
        self.assertIn('email', form.errors)

class CustomLoginFormTests(TestCase):
    def test_role_field_present(self):
        form = CustomLoginForm()
        self.assertIn('role', form.fields)
        self.assertEqual(form.fields['role'].label, "Login as")
