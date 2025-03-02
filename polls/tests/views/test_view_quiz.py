# tests/test_quiz_view.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from models import Quiz

class QuizViewTests(TestCase):
    def setUp(self):
        """Create a test user and some sample quizzes."""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.quiz1 = Quiz.objects.create(title="Sample Quiz 1")
        self.quiz2 = Quiz.objects.create(title="Sample Quiz 2")

    def test_view_quizzes_page(self):
        """Test that the view_quizzes page loads correctly and shows quizzes."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('view_quizzes'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Quiz 1")
        self.assertContains(response, "Sample Quiz 2")
        self.assertContains(response, "Download Report")