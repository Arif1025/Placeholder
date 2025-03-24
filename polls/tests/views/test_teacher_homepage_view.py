from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class TeacherHomeViewTestCase(TestCase):
    """Tests for the teacher home (dashboard) view with the page content."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']  # Load a fixture to set up the test data

    def setUp(self):
        """Setup the test environment by defining the URL and fetching a user."""
        self.url = reverse('teacher_home_interface')  # URL for the teacher's homepage
        self.user = User.objects.get(username='@johndoe')  # Fetch the user used for login

    def test_teacher_home_url(self):
        """Test that the URL for the teacher's homepage is correct."""
        self.assertEqual(self.url, '/')  # Ensure the URL resolves to the correct path

    def test_get_teacher_home(self):
        """Test that the teacher homepage loads properly and displays correct content."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)  # Ensure the page loads with status code 200 (OK)
        self.assertTemplateUsed(response, 'teacher_home_interface.html')  # Ensure the correct template is used

        # Check for key content such as page title and welcome message
        self.assertContains(response, '<h1>Home</h1>')
        self.assertContains(response, 'Welcome, Teacher!')

    def test_get_teacher_home_logged_in(self):
        """Test that logged-in teachers see the homepage without redirection."""
        self.client.login(username=self.user.username, password="Password123")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)  # Ensure the page loads successfully
        self.assertTemplateUsed(response, 'teacher_home_interface.html')  # Ensure the correct template is used

    def test_teacher_home_page_contains_classes_and_polls(self):
        """Test that the homepage contains the teacher's classes and polls."""
        response = self.client.get(self.url)

        # Check if the "Your Classes" section is present
        self.assertContains(response, '<h2>Your Classes</h2>')
        self.assertContains(response, 'Math 101 - Mr. Smith')
        self.assertContains(response, 'History 202 - Ms. Johnson')

        # Check if the "Your Polls" section is present
        self.assertContains(response, '<h2>Your Polls</h2>')
        self.assertContains(response, 'Poll 1: What\'s your favorite topic?')
        self.assertContains(response, 'Poll 2: Feedback on last lesson')

    def test_make_new_poll_button(self):
        """Test that the 'Make New Poll' button is present on the teacher's homepage."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="make-poll-button">Make New Poll</button>')

    def test_logout_button(self):
        """Test that the 'Logout' button is visible on the teacher homepage."""
        response = self.client.get(self.url)

        # Ensure the 'Logout' button is present on the page
        self.assertContains(response, '<button class="logout-button">Logout</button>')

    def test_view_poll_results_button(self):
        """Test that the 'View Poll Results' button is visible and functional."""
        response = self.client.get(self.url)

        # Check if the 'View Poll Results' button is present
        self.assertContains(response, '<button class="btn btn-purple">View Poll Results</button>')

        # Ensure the link for the 'View Poll Results' button works with an example poll ID
        poll_id = 1  # This should be replaced with an actual poll ID you're testing for
        self.assertContains(response, f'href="/polls/{poll_id}/results/"')  # Update with the correct URL structure
