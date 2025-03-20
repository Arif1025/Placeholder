import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from polls.models import Poll, Question, Choice, Response

User = get_user_model()

class PollModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="teacher", password="password123")

    def test_auto_code_generation(self):
        poll = Poll.objects.create(
            title="Poll with auto code",
            description="No code provided initially",
            created_by=self.user
        )
        self.assertIsNotNone(poll.code, "Poll code should be auto-generated.")
        self.assertTrue(len(poll.code) > 0, "Generated code should be non-empty.")

    def test_explicit_code(self):
        poll = Poll.objects.create(
            title="Poll with explicit code",
            description="We assign the code manually",
            created_by=self.user,
            code="CUSTOM123"
        )
        self.assertEqual(poll.code, "CUSTOM123", "Poll should keep our manually assigned code.")

    def test_is_done_default_false(self):
        poll = Poll.objects.create(
            title="New Poll",
            description="Testing is_done default",
            created_by=self.user
        )
        self.assertFalse(poll.is_done, "New poll should be active (is_done=False) by default.")

    def test_poll_str(self):
        poll = Poll.objects.create(
            title="Str check Poll",
            description="Check __str__ method",
            created_by=self.user
        )
        self.assertEqual(str(poll), "Str check Poll")

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