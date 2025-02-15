from django.test import TestCase
from django.urls import reverse


class QuestionPageViewTestCase(TestCase):
    """Tests for the question page view and its elements."""

    def setUp(self):
        self.url = reverse('question_page')  

    def test_question_page_url(self):
        """Test that the URL is correct."""
        self.assertEqual(self.url, '/question_page/') 

    def test_get_question_page(self):
        """Test that the question page loads properly."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'question_page.html')  

        # Check for expected elements in the HTML (e.g., the question and options)
        self.assertContains(response, '<h1>Question 1</h1>')
        self.assertContains(response, 'What is the capital of France?')
        self.assertContains(response, 'Paris')
        self.assertContains(response, 'London')
        self.assertContains(response, 'Berlin')
        self.assertContains(response, 'Madrid')

    def test_logout_button(self):
        """Test that the 'Logout' button is visible on the page."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>')

    def test_navigation_buttons(self):
        """Test that the navigation buttons (Back and Next) are present."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="navigation-button">Back</button>')
        self.assertContains(response, '<button class="navigation-button">Next</button>')

    def test_control_buttons(self):
        """Test that the control buttons (Lock Answer and Show Answer) are present."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="control-button">Lock Answer</button>')
        self.assertContains(response, '<button class="control-button">Show Answer</button>')

    def test_answer_toggle_buttons(self):
        """Test that the Unlock Answer and Hide Answer buttons are present."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="answer-toggle-button">Unlock Answer</button>')
        self.assertContains(response, '<button class="answer-toggle-button">Hide Answer</button>')

        self.assertContains(response, 'background-color: #8e24aa') 

    def test_mobile_responsiveness(self):
        """Test if the page is responsive on smaller screens."""
        response = self.client.get(self.url)
        
        self.assertContains(response, '@media screen and (max-width: 768px)')

    def test_footer(self):
        """Test that the footer is displayed properly with the correct text."""
        response = self.client.get(self.url)

        self.assertContains(response, '&copy; 2025 Polling System')

    def test_question_options(self):
        """Test that the question options are present and correctly rendered."""
        response = self.client.get(self.url)

        # Ensure radio buttons for options are rendered properly
        self.assertContains(response, '<input type="radio" name="answer" value="a">')
        self.assertContains(response, '<input type="radio" name="answer" value="b">')
        self.assertContains(response, '<input type="radio" name="answer" value="c">')
        self.assertContains(response, '<input type="radio" name="answer" value="d">')