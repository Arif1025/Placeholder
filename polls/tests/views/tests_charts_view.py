from django.test import TestCase
from django.urls import reverse

class PollResultsPageViewTestCase(TestCase):
    """Tests for the Poll Results page view and its elements."""

    def setUp(self):
        """Setup for the Poll Results page test by defining the URL."""
        self.url = reverse('charts')  # URL for the poll results page

    def test_poll_results_page_url(self):
        """Test that the URL is correct for the poll results page."""
        self.assertEqual(self.url, '/charts/')  # Ensure the URL resolves to the correct path

    def test_get_poll_results_page(self):
        """Test that the Poll Results page loads correctly and displays the right content."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)  # Ensure the page loads successfully (status 200)
        self.assertTemplateUsed(response, 'charts.html')  # Ensure the correct template is used

        # Check for key content such as page title and poll names
        self.assertContains(response, '<h1>Poll Results</h1>')
        self.assertContains(response, 'Poll 1: What\'s your favorite subject?')
        self.assertContains(response, 'Poll 2: How do you rate the current semester?')
        
        # Ensure the chart canvases are included for displaying poll data
        self.assertContains(response, '<canvas id="pollChart1"></canvas>')
        self.assertContains(response, '<canvas id="pollChart2"></canvas>')

        # Ensure the "Download Report" button is visible
        self.assertContains(response, '<button class="download-button">Download Report</button>')

    def test_poll_chart1_canvas(self):
        """Test that the first poll chart canvas is present on the page."""
        response = self.client.get(self.url)

        self.assertContains(response, '<canvas id="pollChart1"></canvas>')  # Ensure canvas for Poll 1 is present

    def test_poll_chart2_canvas(self):
        """Test that the second poll chart canvas is present on the page."""
        response = self.client.get(self.url)

        self.assertContains(response, '<canvas id="pollChart2"></canvas>')  # Ensure canvas for Poll 2 is present

    def test_logout_button(self):
        """Test that the 'Logout' button is visible on the page."""
        response = self.client.get(self.url)

        # Check that the 'Logout' button exists on the page
        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>')

    def test_back_button(self):
        """Test that the 'Back' button is present and functional on the page."""
        response = self.client.get(self.url)

        # Ensure the 'Back' button links to the previous page correctly
        self.assertContains(response, '<a href="javascript:history.back()" class="back-button">Back</a>')

    def test_footer(self):
        """Test that the footer is displayed correctly with the proper text."""
        response = self.client.get(self.url)

        # Ensure the footer contains the correct copyright information
        self.assertContains(response, '&copy; 2025 Polling System')

    def test_mobile_responsiveness(self):
        """Test if the Poll Results page is responsive on smaller screens."""
        response = self.client.get(self.url)

        # Ensure that responsive media queries are included for small screen devices
        self.assertContains(response, '@media screen and (max-width: 768px)')

    def test_page_elements_styles(self):
        """Test specific styles for page elements like background and button hover styles."""
        response = self.client.get(self.url)

        # Check if specific styles for background color are applied
        self.assertContains(response, 'background-color: #f4f4f4')  # Background color for the page
        self.assertContains(response, 'background-color: #007bff')  # Background color for primary buttons
        self.assertContains(response, 'background-color: #0056b3')  # Hover background color for buttons

        # Check the "Download Report" button styles (check its background color)
        self.assertContains(response, 'background-color: #8e24aa')  # Button color
        self.assertContains(response, 'background-color: #9b4dca')  # Button hover color

    def test_chart_js_inclusion(self):
        """Test if the Chart.js library is included and functional for displaying charts."""
        response = self.client.get(self.url)

        # Ensure the Chart.js script is included on the page
        self.assertContains(response, 'https://cdn.jsdelivr.net/npm/chart.js')

    def test_chart_data_poll1(self):
        """Test that the data for the first poll chart (Poll 1) is correctly passed to the JavaScript."""
        response = self.client.get(self.url)

        # Check that the correct poll data for Poll 1 is included in the JavaScript
        self.assertContains(response, 'labels: [\'Math\', \'Science\', \'History\', \'Art\']')  # Poll 1 labels
        self.assertContains(response, 'data: [10, 5, 3, 2]')  # Poll 1 data values

    def test_chart_data_poll2(self):
        """Test that the data for the second poll chart (Poll 2) is correctly passed to the JavaScript."""
        response = self.client.get(self.url)

        # Check that the correct poll data for Poll 2 is included in the JavaScript
        self.assertContains(response, 'labels: [\'Excellent\', \'Good\', \'Average\', \'Poor\']')  # Poll 2 labels
        self.assertContains(response, 'data: [8, 6, 2, 1]')  # Poll 2 data values