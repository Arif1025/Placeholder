from django.test import TestCase
from polls.forms import QuestionForm
from polls.models import Poll, CustomUser

class QuestionFormTests(TestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.create_user(username='teacher3', password='testpass', role='teacher')
        self.poll = Poll.objects.create(title='Quiz A', description='Desc', created_by=self.teacher, code='QZ123')

    def test_valid_written_question(self):
        form_data = {
            'text': 'What is 2 + 2?',
            'question_type': 'written',
            'correct_answer': '4',
            'options': ''
        }
        form = QuestionForm(data=form_data)
        print("written_question errors:", form.errors)
        self.assertTrue(form.is_valid())

    def test_valid_mcq_question_with_options(self):
        form_data = {
            'text': 'What color is the sky?',
            'question_type': 'mcq',
            'correct_answer': 'Blue',
            'options': 'Blue\nGreen\nRed\nYellow'
        }
        form = QuestionForm(data=form_data)
        print("mcq_question errors:", form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_question_missing_text(self):
        form_data = {
            'text': '',
            'question_type': 'written',
            'correct_answer': 'something',
            'options': ''
        }
        form = QuestionForm(data=form_data)
        print("missing_text errors:", form.errors)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)
