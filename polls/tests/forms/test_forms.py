from django.test import TestCase
from django.contrib.auth import get_user_model
from polls.forms import PollForm, QuestionForm
from polls.models import Poll, Question

User = get_user_model()

class PollFormTest(TestCase):
    """
    Test cases for the PollForm validation.
    """

    def test_valid_poll_form(self):
        """
        Test that the PollForm is valid when provided with a valid title and description.
        """
        form = PollForm(data={"title": "Test Poll", "description": "Test Description"})
        self.assertTrue(form.is_valid())

    def test_invalid_poll_form(self):
        """
        Test that the PollForm is invalid when provided with an empty title and description.
        """
        form = PollForm(data={"title": "", "description": ""})
        self.assertFalse(form.is_valid())

class QuestionFormTest(TestCase):
    """
    Test cases for the QuestionForm validation.
    """

    def test_valid_question_form(self):
        """
        Test that the QuestionForm is valid when a valid question text is provided.
        """
        form = QuestionForm(data={"question_text": "What is your favorite color?"})
        self.assertTrue(form.is_valid())

    def test_invalid_question_form(self):
        """
        Test that the QuestionForm is invalid when the question text is empty.
        """
        form = QuestionForm(data={"question_text": ""})
        self.assertFalse(form.is_valid())
