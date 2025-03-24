from django.contrib.auth.hashers import check_password
from django.test import TestCase
from polls.models import CustomUser
from polls.forms import PasswordForm

class PasswordFormTestCase(TestCase):
    """
    Test cases for the PasswordForm that validates password change functionality.
    """

    def setUp(self):
        """
        Set up a test user and form input data for the password change form.
        """
        self.user = CustomUser.objects.create_user(username='testuser', password='Password123')
        self.form_input = {
            'password': 'Password123',
            'new_password': 'NewPassword123',
            'password_confirmation': 'NewPassword123',
        }

    def test_form_has_necessary_fields(self):
        """
        Test that the PasswordForm contains the necessary fields.
        """
        form = PasswordForm(user=self.user)
        self.assertIn('password', form.fields)
        self.assertIn('new_password', form.fields)
        self.assertIn('password_confirmation', form.fields)

    def test_valid_form(self):
        """
        Test that the PasswordForm is valid when provided with correct data.
        """
        form = PasswordForm(user=self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        """
        Test that the new password must contain at least one uppercase letter.
        """
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = PasswordForm(user=self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        """
        Test that the new password must contain at least one lowercase letter.
        """
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = PasswordForm(user=self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        """
        Test that the new password must contain at least one numeric character.
        """
        self.form_input['new_password'] = 'PasswordABC'
        self.form_input['password_confirmation'] = 'PasswordABC'
        form = PasswordForm(user=self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        """
        Test that the new password and password confirmation must be identical.
        """
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = PasswordForm(user=self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_be_valid(self):
        """
        Test that the current password must be correct.
        """
        self.form_input['password'] = 'WrongPassword123'
        form = PasswordForm(user=self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_contain_user(self):
        """
        Test that the form must be provided with a user to be valid.
        """
        form = PasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_save_form_changes_password(self):
        """
        Test that the form successfully updates the user's password.
        """
        form = PasswordForm(user=self.user, data=self.form_input)
        form.full_clean()
        form.save()
        self.user.refresh_from_db()
        self.assertFalse(check_password('Password123', self.user.password))
        self.assertTrue(check_password('NewPassword123', self.user.password))

    def test_save_userless_form(self):
        """
        Test that saving a form without a user should return False.
        """
        form = PasswordForm(user=None, data=self.form_input)
        form.full_clean()
        result = form.save()
        self.assertFalse(result)
