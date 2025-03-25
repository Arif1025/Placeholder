from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from polls.models import Poll

User = get_user_model()

class StudentConfirmationPageViewTest(TestCase):
    """Tests for the student quiz submission confirmation page."""

    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create_user(
            username="student1", password="Password123", role="student"
        )
        cls.poll = Poll.objects.create(
            title="Test Poll", description="Sample", created_by=cls.student, code="QUIZ123"
        )
        cls.url = reverse('student_confirmation_page', args=[cls.poll.code])
        cls.final_score_url = reverse('final_score_page', args=[cls.poll.code])
        cls.home_url = reverse('student_home_interface')
        cls.login_url = reverse('login_interface')

    def login_student(self):
        self.client.login(username="student1", password="Password123")

    def test_redirects_if_not_logged_in(self):
        """Unauthenticated user is redirected to login."""
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{self.login_url}?next={self.url}")

    def test_confirmation_page_loads_for_authenticated_student(self):
        self.login_student()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "student_confirmation_page.html")
        self.assertContains(response, "<h1>Submission Confirmation</h1>")
        self.assertContains(response, "Your answers have been received")

    def test_context_variables_present(self):
        """Ensure context includes poll and poll_code."""
        self.login_student()
        response = self.client.get(self.url)
        self.assertEqual(response.context["poll"], self.poll)
        self.assertEqual(response.context["poll_code"], self.poll.code)

    def test_results_button_redirects_correctly(self):
        """Ensure button links to final score page."""
        self.login_student()
        response = self.client.get(self.url)
        self.assertContains(response, 'href="/polls/final-score/QUIZ123/"')

    def test_back_to_home_button_correct(self):
        self.login_student()
        response = self.client.get(self.url)
        self.assertContains(response, f'href="{self.home_url}"')
        self.assertContains(response, "Back to Home")

    def test_logout_button_and_positioning(self):
        self.login_student()
        response = self.client.get(self.url)
        self.assertContains(response, 'class="logout-button"')
        self.assertContains(response, "position: fixed")
        self.assertContains(response, "top: 20px")

    def test_styling_and_mobile_responsiveness(self):
        self.login_student()
        response = self.client.get(self.url)
        self.assertContains(response, "background-color: #8e24aa")
        self.assertContains(response, "@media screen and (max-width: 768px)")
        self.assertContains(response, "padding: 10px;")

    def test_invalid_poll_code_returns_404(self):
        """If poll code doesn't match any poll, should raise 404."""
        self.login_student()
        bad_url = reverse('student_confirmation_page', args=["FAKECODE"])
        response = self.client.get(bad_url)
        self.assertEqual(response.status_code, 404)

    def test_back_to_home_button_semantics(self):
        """Ensure proper structure and wording in button."""
        self.login_student()
        response = self.client.get(self.url)
        self.assertContains(response, '<button', html=False)
        self.assertContains(response, 'Back to Home')

    def test_session_quiz_results_if_available(self):
        """Optional: simulate session-based quiz results display logic."""
        self.client.login(username="student1", password="Password123")
        session = self.client.session
        session["quiz_results"] = {
            "poll_code": self.poll.code,
            "score_percentage": 85,
            "correct_count": 4,
            "total_questions": 5,
            "student_answers": []
        }
        session.save()

        response = self.client.get(self.url)
        self.assertContains(response, "Your answers have been received")
