from django.test import TestCase
from django.contrib.auth.models import User
from polls.forms import PollForm, QuestionForm, TeacherRegistrationForm, TeacherLoginForm
from polls.models import Poll, Question

class PollFormTest(TestCase):
    def test_valid_poll_form(self):
        form = PollForm(data={"title": "Test Poll", "description": "Test Description"})
        self.assertTrue(form.is_valid())

    def test_invalid_poll_form(self):
        form = PollForm(data={"title": "", "description": ""})
        self.assertFalse(form.is_valid())

class QuestionFormTest(TestCase):
    def test_valid_question_form(self):
        form = QuestionForm(data={"question_text": "What is your favorite color?"})
        self.assertTrue(form.is_valid())

    def test_invalid_question_form(self):
        form = QuestionForm(data={"question_text": ""})
        self.assertFalse(form.is_valid())

class TeacherRegistrationFormTest(TestCase):
    def test_valid_registration_form(self):
        form = TeacherRegistrationForm(data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!"
        })
        self.assertTrue(form.is_valid())

    def test_invalid_registration_form_password_mismatch(self):
        form = TeacherRegistrationForm(data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "ComplexPass123!",
            "password2": "WrongPass456!"
        })
        self.assertFalse(form.is_valid())

    def test_invalid_registration_form_missing_email(self):
        form = TeacherRegistrationForm(data={
            "username": "testuser",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!"
        })
        self.assertFalse(form.is_valid())

class TeacherLoginFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_valid_login_form(self):
        form = TeacherLoginForm(data={"username": "testuser", "password": "testpassword"})
        self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):
        form = TeacherLoginForm(data={"username": "", "password": ""})
        self.assertFalse(form.is_valid())