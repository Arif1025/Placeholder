from django.test import TestCase
from polls.forms import ChoiceForm
from polls.models import Question, Poll, CustomUser

class ChoiceFormTests(TestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.create_user(username='teacher4', password='testpass', role='teacher')
        self.poll = Poll.objects.create(title='Poll B', created_by=self.teacher)
        self.question = Question.objects.create(poll=self.poll, text='MCQ?', question_type='mcq')

    def test_valid_choice_form(self):
        form = ChoiceForm(data={'text': 'Option A'})
        self.assertTrue(form.is_valid())

    def test_blank_choice_fails(self):
        form = ChoiceForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)