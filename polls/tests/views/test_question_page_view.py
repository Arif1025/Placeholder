from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

User = get_user_model()

class QuestionTemplateViewTests(TestCase):
    """Tests for the question_template view (quiz display page)."""

    def setUp(self):
        self.url = reverse("question_template")

    def test_question_template_url(self):
        """URL should resolve correctly."""
        self.assertEqual(resolve(self.url).view_name, "question_template")

    def test_question_template_renders_correctly(self):
        """Test that the question template loads and uses the right template."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "question_template.html")

    def test_core_content_displayed(self):
        """Ensure basic expected content exists (question block, options)."""
        response = self.client.get(self.url)

        # Headings and structure
        self.assertContains(response, 'Question 1')
        self.assertContains(response, 'What is the capital of France?', status_code=200)

        # Answer options (general content)
        for option in ['Paris', 'London', 'Berlin', 'Madrid']:
            self.assertContains(response, option)

        # Radio buttons
        for value in ['a', 'b', 'c', 'd']:
            self.assertContains(response, f'<input type="radio" name="answer" value="{value}"', html=False)

    def test_quiz_control_buttons_exist(self):
        """Ensure all navigation and quiz control buttons are rendered."""
        response = self.client.get(self.url)

        buttons = [
            "Lock Answer", "Unlock Answer",
            "Show Answer", "Hide Answer",
            "Back", "Next", "Leave Quiz", "Logout"
        ]
        for button in buttons:
            self.assertContains(response, button)

    def test_logout_button_html_structure(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>')

    def test_leave_quiz_button_has_correct_redirect(self):
        """Leave quiz button must contain correct link (even if JS-based)."""
        response = self.client.get(self.url)
        self.assertContains(response, 'action="/polls/leave-quiz/"')

    def test_responsive_styles_exist(self):
        """Checks for responsive styles for mobile screens."""
        response = self.client.get(self.url)
        self.assertContains(response, "@media screen and (max-width: 768px)")

    def test_footer_displayed(self):
        """Footer text is shown."""
        response = self.client.get(self.url)
        self.assertContains(response, "&copy; 2025 Polling System")

    def test_answer_toggle_styling(self):
        """Ensure answer toggle buttons have specific styling (e.g. purple)"""
        response = self.client.get(self.url)
        self.assertContains(response, 'background-color: #8e24aa')
