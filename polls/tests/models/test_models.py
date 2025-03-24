import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from polls.models import Poll, Question, Choice, Response

User = get_user_model()

class PollModelTest(TestCase):
    """
    Test cases for the Poll model, including code generation, default values, and string representation.
    """

    def setUp(self):
        """
        Set up a test user for the poll model tests.
        """
        self.user = User.objects.create_user(username="teacher", password="password123")

    def test_auto_code_generation(self):
        """
        Test that the poll's code is auto-generated when not explicitly provided.
        """
        poll = Poll.objects.create(
            title="Poll with auto code",
            description="No code provided initially",
            created_by=self.user
        )
        self.assertIsNotNone(poll.code, "Poll code should be auto-generated.")
        self.assertTrue(len(poll.code) > 0, "Generated code should be non-empty.")

    def test_explicit_code(self):
        """
        Test that a manually assigned poll code is retained.
        """
        poll = Poll.objects.create(
            title="Poll with explicit code",
            description="We assign the code manually",
            created_by=self.user,
            code="CUSTOM123"
        )
        self.assertEqual(poll.code, "CUSTOM123", "Poll should keep our manually assigned code.")

    def test_is_done_default_false(self):
        """
        Test that the default value of is_done is False when a new poll is created.
        """
        poll = Poll.objects.create(
            title="New Poll",
            description="Testing is_done default",
            created_by=self.user
        )
        self.assertFalse(poll.is_done, "New poll should be active (is_done=False) by default.")

    def test_poll_str(self):
        """
        Test the string representation of the Poll model.
        """
        poll = Poll.objects.create(
            title="Str check Poll",
            description="Check __str__ method",
            created_by=self.user
        )
        self.assertEqual(str(poll), "Str check Poll")

class QuestionModelTest(TestCase):
    """
    Test cases for the Question model, including creation and string representation.
    """
    
    def setUp(self):
        """
        Set up a test user, poll, and question for the question model tests.
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.poll = Poll.objects.create(title="Test Poll", description="Test Description", created_by=self.user)
        self.question = Question.objects.create(poll=self.poll, question_text="What is your favorite color?")

    def test_question_creation(self):
        """
        Test that a question is correctly created and associated with a poll.
        """
        self.assertEqual(self.question.poll, self.poll)
        self.assertEqual(self.question.question_text, "What is your favorite color?")

    def test_question_str(self):
        """
        Test the string representation of the Question model.
        """
        self.assertEqual(str(self.question), "What is your favorite color?")

class ChoiceModelTest(TestCase):
    """
    Test cases for the Choice model, including creation and string representation.
    """
    
    def setUp(self):
        """
        Set up a test user, poll, question, and choice for the choice model tests.
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.poll = Poll.objects.create(title="Test Poll", description="Test Description", created_by=self.user)
        self.question = Question.objects.create(poll=self.poll, question_text="What is your favorite color?")
        self.choice = Choice.objects.create(question=self.question, choice_text="Blue")

    def test_choice_creation(self):
        """
        Test that a choice is correctly created and associated with a question.
        """
        self.assertEqual(self.choice.question, self.question)
        self.assertEqual(self.choice.choice_text, "Blue")

    def test_choice_str(self):
        """
        Test the string representation of the Choice model.
        """
        self.assertEqual(str(self.choice), "Blue")

class ResponseModelTest(TestCase):
    """
    Test cases for the Response model, including creation, relationships, and string representation.
    """
    
    def setUp(self):
        """
        Set up a test user, poll, question, choice, and response for the response model tests.
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.poll = Poll.objects.create(title="Test Poll", description="Test Description", created_by=self.user)
        self.question = Question.objects.create(poll=self.poll, question_text="What is your favorite color?")
        self.choice = Choice.objects.create(question=self.question, choice_text="Blue")
        self.response = Response.objects.create(user=self.user, question=self.question, choice=self.choice)

    def test_response_creation(self):
        """
        Test that a response is correctly created and associated with a user, question, and choice.
        """
        self.assertEqual(self.response.user, self.user)
        self.assertEqual(self.response.question, self.question)
        self.assertEqual(self.response.choice, self.choice)
        self.assertIsNotNone(self.response.submitted_at)

    def test_response_str(self):
        """
        Test the string representation of the Response model.
        """
        self.assertEqual(str(self.response), f"{self.user} - {self.question} - {self.choice}")
