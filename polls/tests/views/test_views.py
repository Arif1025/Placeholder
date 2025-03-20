from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from polls.models import Poll, Question, Response, Choice
from django.core.files.uploadedfile import SimpleUploadedFile
import csv
import io

User = get_user_model()

class ViewTests(TestCase):
    """Tests for various views related to the Polling System."""

    def setUp(self):
        """Set up test data including user, poll, question, and choice."""
        self.client = Client()
        self.user = User.objects.create_user(username="teacheruser", password="StrongPass123")
        self.poll = Poll.objects.create(title="Test Poll", description="Poll description", created_by=self.user)
        self.question = Question.objects.create(question_text="Test Question", poll=self.poll)
        self.choice = Choice.objects.create(question=self.question, choice_text="Sample Choice")

    def test_index_view(self):
        """Test the index view loads successfully."""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)  # Should return status 200
        self.assertContains(response, "Hello, this is the index view.")  # Check for specific content

    def test_homepage_view(self):
        """Test the homepage view loads successfully."""
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)  # Should return status 200
        self.assertContains(response, "Hello! This is the homepage at the root URL.")  # Check for content

    def test_register_teacher_view(self):
        """Test teacher registration process."""
        response = self.client.post(reverse("register_teacher"), {
            "username": "newteacher",
            "email": "newteacher@example.com",
            "password1": "TestPass123",
            "password2": "TestPass123"
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration
        self.assertTrue(User.objects.filter(username="newteacher").exists())  # Check if new user was created

    def test_login_teacher_view(self):
        """Test teacher login functionality."""
        response = self.client.post(reverse("login_teacher"), {
            "username": "teacheruser",
            "password": "StrongPass123"
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login

    def test_logout_teacher_view(self):
        """Test teacher logout functionality."""
        self.client.login(username="teacheruser", password="StrongPass123")
        response = self.client.get(reverse("logout_teacher"))
        self.assertEqual(response.status_code, 302)  # Should redirect after logout

    def test_poll_list_view(self):
        """Test the poll list view displays polls correctly."""
        response = self.client.get(reverse("poll_list"))
        self.assertEqual(response.status_code, 200)  # Should return status 200
        self.assertContains(response, "Test Poll")  # Ensure poll title is displayed

    def test_create_poll_view(self):
        """Test creating a new poll."""
        self.client.login(username="teacheruser", password="StrongPass123")
        response = self.client.post(reverse("create_poll"), {"title": "New Poll", "description": "New poll description"})
        self.assertEqual(response.status_code, 302)  # Should redirect after creating poll
        self.assertTrue(Poll.objects.filter(title="New Poll").exists())  # Check if new poll was created

    def test_delete_poll_view(self):
        """Test deleting an existing poll."""
        self.client.login(username="teacheruser", password="StrongPass123")
        response = self.client.post(reverse("delete_poll", args=[self.poll.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after deleting poll
        self.assertFalse(Poll.objects.filter(id=self.poll.id).exists())  # Check if poll was deleted

    def test_create_question_view(self):
        """Test creating a new question for a poll."""
        self.client.login(username="teacheruser", password="StrongPass123")
        response = self.client.post(reverse("create_question", args=[self.poll.id]), {"question_text": "New Question"})
        self.assertEqual(response.status_code, 302)  # Should redirect after creating question
        self.assertTrue(Question.objects.filter(question_text="New Question").exists())  # Check if question was created

    def test_delete_question_view(self):
        """Test deleting an existing question."""
        self.client.login(username="teacheruser", password="StrongPass123")
        response = self.client.post(reverse("delete_question", args=[self.question.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after deleting question
        self.assertFalse(Question.objects.filter(id=self.question.id).exists())  # Check if question was deleted

    def test_export_poll_responses_csv_view(self):
        """Test CSV export functionality for poll responses."""
        self.client.login(username="teacheruser", password="StrongPass123")

        # Create a response for the poll
        Response.objects.create(user=self.user, question=self.question, choice=self.choice)

        response = self.client.get(reverse("export_poll_responses", args=[self.poll.id]))
        self.assertEqual(response.status_code, 200)  # Should return status 200
        self.assertEqual(response["Content-Type"], "text/csv")  # Ensure content type is CSV

        # Read the CSV data
        csv_data = response.content.decode("utf-8")
        csv_reader = csv.reader(io.StringIO(csv_data))
        csv_rows = list(csv_reader)

        # Check CSV headers
        expected_headers = ["Student", "Question", "Selected Choice", "Submitted At"]
        self.assertEqual(csv_rows[0], expected_headers)  # Check headers

        # Check response content in CSV
        self.assertEqual(csv_rows[1][0], self.user.username)  # Username is correct
        self.assertEqual(csv_rows[1][1], self.question.question_text)  # Question text is correct
        self.assertEqual(csv_rows[1][2], self.choice.choice_text)  # Choice text is correct
        self.assertTrue(csv_rows[1][3])  # Submitted timestamp exists