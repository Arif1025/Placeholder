from django.test import TestCase
from django.contrib.auth import get_user_model
from polls.forms import PollForm, QuestionForm
from polls.models import Poll, Question

User = get_user_model()

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