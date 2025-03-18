from django.test import TestCase
from django.urls import reverse

class PollResultsPageViewTestCase(TestCase):
    """Tests for the Poll Results page view and its elements."""

    def setUp(self):
        self.url = reverse('charts')  # URL for the poll results page

    def test_poll_results_page_url(self):
        """Test that the URL is correct."""
        self.assertEqual(self.url, '/charts/')

    def test_get_poll_results_page(self):
        """Test that the Poll Results page loads properly."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'charts.html')

        # Check for expected elements in the HTML (chart canvas and page title)
        self.assertContains(response, '<h1>Poll Results</h1>')
        self.assertContains(response, 'Poll 1: What\'s your favorite subject?')
        self.assertContains(response, 'Poll 2: How do you rate the current semester?')
        self.assertContains(response, '<canvas id="pollChart1"></canvas>')
        self.assertContains(response, '<canvas id="pollChart2"></canvas>')

    def test_poll_chart1_canvas(self):
        """Test that the first poll chart canvas is present."""
        response = self.client.get(self.url)

        self.assertContains(response, '<canvas id="pollChart1"></canvas>')

    def test_poll_chart2_canvas(self):
        """Test that the second poll chart canvas is present."""
        response = self.client.get(self.url)

        self.assertContains(response, '<canvas id="pollChart2"></canvas>')

    def test_logout_button(self):
        """Test that the 'Logout' button is visible on the page."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>')

    def test_back_button(self):
        """Test that the 'Back' button is present and has the correct link."""
        response = self.client.get(self.url)

        # Check if the back button exists
        self.assertContains(response, '<a href="javascript:history.back()" class="back-button">Back</a>')

    def test_footer(self):
        """Test that the footer is displayed properly with the correct text."""
        response = self.client.get(self.url)

        self.assertContains(response, '&copy; 2025 Polling System')

    def test_mobile_responsiveness(self):
        """Test if the page is responsive on smaller screens."""
        response = self.client.get(self.url)

        self.assertContains(response, '@media screen and (max-width: 768px)')

    def test_page_elements_styles(self):
        """Test specific styles for the page elements."""
        response = self.client.get(self.url)

        # Check background color and button hover styles in the response (basic checks)
        self.assertContains(response, 'background-color: #f4f4f4')
        self.assertContains(response, 'background-color: #007bff')  # Button background color
        self.assertContains(response, 'background-color: #0056b3')  # Button hover color

    def test_chart_js_inclusion(self):
        """Test if Chart.js library is included and functional."""
        response = self.client.get(self.url)

        self.assertContains(response, 'https://cdn.jsdelivr.net/npm/chart.js')

    def test_chart_data_poll1(self):
        """Test that the data for Poll 1 chart is correct in the JavaScript."""
        response = self.client.get(self.url)

        # Check that the JavaScript contains the correct labels and data for Poll 1
        self.assertContains(response, 'labels: [\'Math\', \'Science\', \'History\', \'Art\']')
        self.assertContains(response, 'data: [10, 5, 3, 2]')  # Example data for Poll 1

    def test_chart_data_poll2(self):
        """Test that the data for Poll 2 chart is correct in the JavaScript."""
        response = self.client.get(self.url)

        # Check that the JavaScript contains the correct labels and data for Poll 2
        self.assertContains(response, 'labels: [\'Excellent\', \'Good\', \'Average\', \'Poor\']')
        self.assertContains(response, 'data: [8, 6, 2, 1]')  # Example data for Poll 2
