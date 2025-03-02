from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class FinalScoreViewTestCase(TestCase):
    """
    Tests for the final score view.
    """

    def setUp(self):
        """Set up test user and URL."""
        self.user = get_user_model().objects.create_user(username="testuser", password="Password123")
        self.url = reverse("final_score")  # Final score page URL

    def test_redirects_if_not_logged_in(self):
        """Test redirect to login if not logged in."""
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)  # Should not return 200
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")  # Redirect to login

    def test_view_renders_for_logged_in_user(self):
        """Test page renders correctly for logged-in users."""
        self.client.login(username="testuser", password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Page loads with status 200
        self.assertTemplateUsed(response, "final_score_page.html")  # Correct template used
        self.assertContains(response, "Final Score")  # Page title exists
        self.assertContains(response, "Your Score")  # Score section exists

    def test_html_contains_questions_and_answers(self):
        """Test that question and answers are displayed correctly."""
        self.client.login(username="testuser", password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, "What is the capital of France?")  # Question shown
        self.assertContains(response, "Correct: Paris")  # Correct answer shown
        self.assertContains(response, "Wrong: Earth (Correct Answer: Jupiter)")  # Incorrect answer shown

    def test_logout_button_exists(self):
        """Test that the logout button is present."""
        self.client.login(username="testuser", password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>')  # Logout button exists

    def test_navigation_buttons_exist(self):
        """Test that navigation buttons are present."""
        self.client.login(username="testuser", password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, "Back to Home")  # 'Back to Home' button exists
        self.assertContains(response, "Try Again")  # 'Try Again' button exists