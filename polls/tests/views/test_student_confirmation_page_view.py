from django.test import TestCase
from django.urls import reverse


class StudentConfirmationPageViewTestCase(TestCase):
    """Tests for the confirmation page view and its elements."""

    def setUp(self):
        self.url = reverse('student_confirmation_page') 

    def test_student_confirmation_page_url(self):
        """Test that the URL is correct."""
        self.assertEqual(self.url, '/student_confirmation_page/') 

    def test_get_student_confirmation_page(self):
        """Test that the confirmation page loads properly."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_confirmation_page.html') 

        self.assertContains(response, '<h1>Submission Confirmation</h1>')
        self.assertContains(response, 'Thank you! Your answers have been received.')
        self.assertContains(response, 'Click below to view your results.')

    def test_logout_button(self):
        """Test that the 'Logout' button is visible on the page."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>')

    def test_show_results_button(self):
        """Test that the 'Show My Results' button is visible on the page."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="navigation-button" onclick="window.location.href=\'final_score_page.html\'">Show My Results</button>')

    def test_footer(self):
        """Test that the footer is displayed properly with the correct text."""
        response = self.client.get(self.url)

        self.assertContains(response, '&copy; 2025 Polling System')

    def test_mobile_responsiveness(self):
        """Test if the page is responsive on smaller screens."""
        response = self.client.get(self.url)
        
        self.assertContains(response, '@media screen and (max-width: 768px)')

    def test_navigation_buttons(self):
        """Test that the navigation button is present and redirects to the correct results page."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="navigation-button" onclick="window.location.href=\'final_score_page.html\'">Show My Results</button>')

    def test_logout_button_position(self):
        """Test that the logout button appears in the top-right corner of the page."""
        response = self.client.get(self.url)

        self.assertContains(response, 'position: fixed; top: 20px; right: 20px;')  

    def test_confirmation_message(self):
        """Test that the confirmation message is properly displayed."""
        response = self.client.get(self.url)

        self.assertContains(response, 'Your answers have been received.')
        self.assertContains(response, 'Click below to view your results.')

    def test_navigation_button_style(self):
        """Test that the navigation button has the correct background color."""
        response = self.client.get(self.url)

        self.assertContains(response, 'background-color: #8e24aa') 

    def test_mobile_responsiveness_footer(self):
        """Test that the footer appears correctly on smaller screens."""
        response = self.client.get(self.url)

        self.assertContains(response, '@media screen and (max-width: 768px)')
        self.assertContains(response, 'padding: 10px;')

    # New tests for the "Back to Home" button
    def test_back_to_home_button(self):
        """Test that the 'Back to Home' button is visible on the page."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="back-to-home-button">Back to Home</button>')

    def test_back_to_home_button_link(self):
        """Test that the 'Back to Home' button links to the correct home page."""
        response = self.client.get(self.url)

        self.assertContains(response, 'href="{% url \'student_home_interface\' %}"')

    def test_back_to_home_button_position(self):
        """Test that the 'Back to Home' button is positioned at the top left of the page."""
        response = self.client.get(self.url)

        self.assertContains(response, 'position: fixed; top: 20px; left: 20px;')

    def test_back_to_home_button_style(self):
        """Test that the 'Back to Home' button has the correct background color."""
        response = self.client.get(self.url)

        self.assertContains(response, 'background-color: #8e24aa')

