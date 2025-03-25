from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from polls.models import Poll, StudentQuizResult
from django.utils import timezone

User = get_user_model()

class FinalScoreViewTestCase(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username="testuser", password="Password123", role='student')
        self.poll = Poll.objects.create(title="Geography Quiz", description="Test quiz", created_by=self.student, code="TEST123")
        self.result = StudentQuizResult.objects.create(
            student=self.student,
            poll=self.poll,
            score=3,
            total_questions=5,
            submitted_at=timezone.now()
        )
        self.url = reverse("final_score_page", kwargs={"poll_code": self.poll.code})

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/polls/login_interface"))

    def test_redirects_if_session_missing(self):
        self.client.login(username="testuser", password="Password123")
        response = self.client.get(self.url)
        # Should redirect to home because session['quiz_results'] is missing
        self.assertRedirects(response, reverse("student_home_interface"))

    def test_view_renders_with_quiz_results(self):
        self.client.login(username="testuser", password="Password123")
        session = self.client.session
        session["quiz_results"] = {
            "poll_code": self.poll.code,
            "score_percentage": 60,
            "correct_count": 3,
            "total_questions": 5,
            "student_answers": [
                {
                    "question": "What is the capital of France?",
                    "user_answer": "Paris",
                    "correct_answer": "Paris",
                    "is_correct": True
                },
                {
                    "question": "Biggest planet?",
                    "user_answer": "Earth",
                    "correct_answer": "Jupiter",
                    "is_correct": False
                }
            ]
        }
        session.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "final_score_page.html")
        self.assertContains(response, "What is the capital of France?")
        self.assertContains(response, "Paris")
        self.assertContains(response, "Earth")
        self.assertContains(response, "Jupiter")
        self.assertContains(response, "Score: 60%")

    def test_logout_button_exists(self):
        self.client.login(username="testuser", password="Password123")
        session = self.client.session
        session["quiz_results"] = {
            "poll_code": self.poll.code,
            "score_percentage": 60,
            "correct_count": 3,
            "total_questions": 5,
            "student_answers": []
        }
        session.save()

        response = self.client.get(self.url)
        self.assertContains(response, "Logout")

    def test_navigation_buttons_exist(self):
        self.client.login(username="testuser", password="Password123")
        session = self.client.session
        session["quiz_results"] = {
            "poll_code": self.poll.code,
            "score_percentage": 60,
            "correct_count": 3,
            "total_questions": 5,
            "student_answers": []
        }
        session.save()

        response = self.client.get(self.url)
        self.assertContains(response, "Back")

    def test_back_button_exists(self):
        self.client.login(username="testuser", password="Password123")
        session = self.client.session
        session["quiz_results"] = {
            "poll_code": self.poll.code,
            "score_percentage": 60,
            "correct_count": 3,
            "total_questions": 5,
            "student_answers": []
        }
        session.save()

        response = self.client.get(self.url)
        self.assertContains(response, "class=\"back-button\"")
