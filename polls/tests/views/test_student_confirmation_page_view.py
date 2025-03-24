from django.test import TestCase
from django.urls import reverse


class StudentConfirmationPageViewTestCase(TestCase):
    """Tests for the student confirmation page and its elements."""
    
    def setUp(self):
        """Setup the test URL for the confirmation page."""
        self.url = reverse('student_confirmation_page')  # URL for the student confirmation page

    def test_student_confirmation_page_url(self):
        """Test that the URL is correctly resolved."""
        self.assertEqual(self.url, '/student_confirmation_page/')  # Check if URL matches expected path

    def test_get_student_confirmation_page(self):
        """Test that the confirmation page loads correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Ensure a successful response (200 OK)
        self.assertTemplateUsed(response, 'student_confirmation_page.html')  # Ensure correct template is used

        # Check for expected content on the page
        self.assertContains(response, '<h1>Submission Confirmation</h1>')
        self.assertContains(response, 'Thank you! Your answers have been received.')
        self.assertContains(response, 'Click below to view your results.')

    def test_logout_button(self):
        """Test that the 'Logout' button is present on the page."""
        response = self.client.get(self.url)
        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>')

    def test_show_results_button(self):
        """Test that the 'Show My Results' button is visible and functional."""
        response = self.client.get(self.url)
        self.assertContains(response, '<button class="navigation-button" onclick="window.location.href=\'final_score_page.html\'">Show My Results</button>')

    def test_footer(self):
        """Test that the footer appears correctly with expected content."""
        response = self.client.get(self.url)
        self.assertContains(response, '&copy; 2025 Polling System')

    def test_mobile_responsiveness(self):
        """Test that the page is responsive and adapts on smaller screens."""
        response = self.client.get(self.url)
        self.assertContains(response, '@media screen and (max-width: 768px)')  # Check for mobile responsiveness

    def test_navigation_buttons(self):
        """Test that navigation buttons are visible and function correctly."""
        response = self.client.get(self.url)
        self.assertContains(response, '<button class="navigation-button" onclick="window.location.href=\'final_score_page.html\'">Show My Results</button>')

    def test_logout_button_position(self):
        """Test that the logout button is positioned correctly on the page."""
        response = self.client.get(self.url)
        self.assertContains(response, 'position: fixed; top: 20px; right: 20px;')  # Check for top-right positioning

    def test_confirmation_message(self):
        """Test that the confirmation message is correctly displayed."""
        response = self.client.get(self.url)
        self.assertContains(response, 'Your answers have been received.')
        self.assertContains(response, 'Click below to view your results.')

    def test_navigation_button_style(self):
        """Test that the 'Show My Results' button has the correct styling."""
        response = self.client.get(self.url)
        self.assertContains(response, 'background-color: #8e24aa')  # Check for the correct background color

    def test_mobile_responsiveness_footer(self):
        """Test that the footer appears correctly on smaller screens."""
        response = self.client.get(self.url)
        self.assertContains(response, '@media screen and (max-width: 768px)')  # Check for mobile footer styling
        self.assertContains(response, 'padding: 10px;')  # Check padding styling

    # New tests for the "Back to Home" button
    def test_back_to_home_button(self):
        """Test that the 'Back to Home' button is visible on the page."""
        response = self.client.get(self.url)
        self.assertContains(response, '<button class="back-to-home-button">Back to Home</button>')

    def test_back_to_home_button_link(self):
        """Test that the 'Back to Home' button links to the correct home page."""
        response = self.client.get(self.url)
        self.assertContains(response, 'href="{% url \'student_home_interface\' %}"')  # Check for correct URL link

    def test_back_to_home_button_position(self):
        """Test that the 'Back to Home' button is correctly positioned."""
        response = self.client.get(self.url)
        self.assertContains(response, 'position: fixed; top: 20px; left: 20px;')  # Check top-left positioning

    def test_back_to_home_button_style(self):
        """Test that the 'Back to Home' button has the correct background color."""
        response = self.client.get(self.url)
        self.assertContains(response, 'background-color: #8e24aa')  # Check button color
