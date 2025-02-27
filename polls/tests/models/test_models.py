from django.test import TestCase
from django.contrib.auth.models import User
from polls.models import Poll, Question, Choice, Response

class PollModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.poll = Poll.objects.create(title="Test Poll", description="Test Description", created_by=self.user)

    def test_poll_creation(self):
        self.assertEqual(self.poll.title, "Test Poll")
        self.assertEqual(self.poll.created_by, self.user)
        self.assertIsNotNone(self.poll.created_at)

    def test_poll_str(self):
        self.assertEqual(str(self.poll), "Test Poll")

class QuestionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.poll = Poll.objects.create(title="Test Poll", description="Test Description", created_by=self.user)
        self.question = Question.objects.create(poll=self.poll, question_text="What is your favorite color?")

    def test_question_creation(self):
        self.assertEqual(self.question.poll, self.poll)
        self.assertEqual(self.question.question_text, "What is your favorite color?")

    def test_question_str(self):
        self.assertEqual(str(self.question), "What is your favorite color?")

class ChoiceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.poll = Poll.objects.create(title="Test Poll", description="Test Description", created_by=self.user)
        self.question = Question.objects.create(poll=self.poll, question_text="What is your favorite color?")
        self.choice = Choice.objects.create(question=self.question, choice_text="Blue")

    def test_choice_creation(self):
        self.assertEqual(self.choice.question, self.question)
        self.assertEqual(self.choice.choice_text, "Blue")

    def test_choice_str(self):
        self.assertEqual(str(self.choice), "Blue")

class ResponseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.poll = Poll.objects.create(title="Test Poll", description="Test Description", created_by=self.user)
        self.question = Question.objects.create(poll=self.poll, question_text="What is your favorite color?")
        self.choice = Choice.objects.create(question=self.question, choice_text="Blue")
        self.response = Response.objects.create(user=self.user, question=self.question, choice=self.choice)

    def test_response_creation(self):
        self.assertEqual(self.response.user, self.user)
        self.assertEqual(self.response.question, self.question)
        self.assertEqual(self.response.choice, self.choice)
        self.assertIsNotNone(self.response.submitted_at)

    def test_response_str(self):
        self.assertEqual(str(self.response), f"{self.user} - {self.question} - {self.choice}")