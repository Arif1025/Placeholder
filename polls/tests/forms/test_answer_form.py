from django.test import TestCase
from polls.forms import AnswerForm
from polls.models import Poll, Question, Choice, CustomUser

class AnswerFormTests(TestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.create_user(username='teacher5', password='testpass', role='teacher')
        self.poll = Poll.objects.create(title='Poll C', created_by=self.teacher)
        self.mcq_question = Question.objects.create(poll=self.poll, text='Pick one', question_type='mcq')
        self.written_question = Question.objects.create(poll=self.poll, text='Explain gravity', question_type='written')
        Choice.objects.create(question=self.mcq_question, text='Option 1', is_correct=True)
        Choice.objects.create(question=self.mcq_question, text='Option 2', is_correct=False)

    def test_answer_form_for_written_question(self):
        form = AnswerForm(question=self.written_question)
        self.assertIn('answer', form.fields)
        self.assertEqual(form.fields['answer'].widget.__class__.__name__, 'Textarea')

    def test_answer_form_for_mcq_question(self):
        form = AnswerForm(question=self.mcq_question)
        self.assertIn('answer', form.fields)
        self.assertEqual(form.fields['answer'].widget.__class__.__name__, 'RadioSelect')
        self.assertEqual(len(form.fields['answer'].choices), 2)