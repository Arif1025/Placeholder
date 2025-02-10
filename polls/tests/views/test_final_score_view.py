from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class FinalScoreViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="Password123")
        self.url = reverse("final_score")

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_view_renders_for_logged_in_user(self):
        self.client.login(username="testuser", password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "final_score_page.html")
        self.assertContains(response, "Final Score")  # Page title check
        self.assertContains(response, "Your Score")  # Ensuring score section exists

    def test_html_contains_questions_and_answers(self):
        self.client.login(username="testuser", password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, "What is the capital of France?")
        self.assertContains(response, "Correct: Paris")
        self.assertContains(response, "Wrong: Earth (Correct Answer: Jupiter)")

    def test_logout_button_exists(self):
        self.client.login(username="testuser", password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>')

    def test_navigation_buttons_exist(self):
        self.client.login(username="testuser", password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, "Back to Home")
        self.assertContains(response, "Try Again")