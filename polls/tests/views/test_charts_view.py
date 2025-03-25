from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from polls.models import Poll, Question, Choice, StudentResponse

User = get_user_model()

class ViewPollResultsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create users
        self.teacher = User.objects.create_user(username='teach1', password='testpass123', role='teacher')
        self.student = User.objects.create_user(username='stud1', password='pass123', role='student')

        # Login as teacher
        self.client.login(username='teach1', password='testpass123')

        # Create a poll
        self.poll = Poll.objects.create(title='Math Quiz', created_by=self.teacher)

        # MCQ question
        self.mcq_question = Question.objects.create(
            poll=self.poll, text='What is 2+2?', question_type='mcq'
        )
        self.correct_mcq = Choice.objects.create(question=self.mcq_question, text='4', is_correct=True)
        Choice.objects.create(question=self.mcq_question, text='3', is_correct=False)
        StudentResponse.objects.create(student=self.student, question=self.mcq_question, response='4')

        # Written question
        self.written_question = Question.objects.create(
            poll=self.poll, text='Define gravity.', question_type='written', correct_answer='Force'
        )
        StudentResponse.objects.create(student=self.student, question=self.written_question, response='Force')

    def test_view_poll_results_renders_correctly(self):
        url = reverse('view_poll_results', args=[self.poll.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'charts.html')

        self.assertContains(response, 'What is 2+2?')
        self.assertContains(response, 'Define gravity.')

        questions_data = response.context['questions_data']
        self.assertEqual(len(questions_data), 2)

        mcq_data = next((q for q in questions_data if q['question_text'] == 'What is 2+2?'), None)
        written_data = next((q for q in questions_data if q['question_text'] == 'Define gravity.'), None)

        self.assertIsNotNone(mcq_data)
        self.assertEqual(mcq_data['correct_choice'], '4')
        self.assertEqual(mcq_data['correct_count'], 1)
        self.assertEqual(mcq_data['wrong_count'], 0)

        self.assertIsNotNone(written_data)
        self.assertEqual(written_data['correct_choice'], 'Force')
        self.assertEqual(written_data['correct_count'], 1)

    def test_redirects_if_not_logged_in(self):
        self.client.logout()
        url = reverse('view_poll_results', args=[self.poll.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url.lower())

    def test_student_can_view_poll_results(self):
        self.client.logout()
        self.client.login(username='stud1', password='pass123')
        url = reverse('view_poll_results', args=[self.poll.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.poll.title)
        self.assertContains(response, self.mcq_question.text)
        self.assertContains(response, self.written_question.text)

    def test_view_poll_results_with_no_responses(self):
        poll = Poll.objects.create(title='Empty Quiz', created_by=self.teacher)
        q = Question.objects.create(poll=poll, text='Unanswered?', question_type='written', correct_answer='Nothing')

        url = reverse('view_poll_results', args=[poll.id])
        response = self.client.get(url)
        self.assertContains(response, 'Unanswered?')

        questions_data = response.context['questions_data']
        self.assertEqual(questions_data[0]['correct_count'], 0)
        self.assertEqual(questions_data[0]['wrong_count'], 0)
        self.assertEqual(len(questions_data[0]['responses']), 0)
