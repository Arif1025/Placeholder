from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentHomeViewTestCase(TestCase):
    """Tests for the student home (dashboard) view with the page content."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']  # Load the fixture to set up test data

    def setUp(self):
        """Set up the test by defining the URL and fetching the user."""
        self.url = reverse('student_home_interface')  # URL for the student home page
        self.user = User.objects.get(username='@johndoe')  # Retrieve the user from the database

    def test_student_home_url(self):
        """Test that the URL is correctly resolved to the homepage."""
        self.assertEqual(self.url, '/')  # Check if the home page URL is correct

    def test_get_student_home(self):
        """Test that the student homepage (dashboard) loads properly."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)  # Ensure the page loads with status code 200 (OK)
        self.assertTemplateUsed(response, 'student_home_interface.html')  # Ensure the correct template is used

        # Check for key content that should be on the page (e.g., title and welcome message)
        self.assertContains(response, '<h1>Home</h1>')
        self.assertContains(response, 'Welcome, John Doe!')

    def test_get_student_home_logged_in(self):
        """Test that logged-in students can access the homepage without redirection."""
        self.client.login(username=self.user.username, password="Password123")  # Log the user in

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)  # Ensure successful login and homepage load
        self.assertTemplateUsed(response, 'student_home_interface.html')  # Ensure the correct template is used

    def test_student_home_page_contains_classes_and_polls(self):
        """Test that the homepage displays the student's classes and polls."""
        response = self.client.get(self.url)

        # Check if the "Your Classes" section is present
        self.assertContains(response, '<h2>Your Classes</h2>')
        self.assertContains(response, 'Math 101 - Mr. Smith')
        self.assertContains(response, 'History 202 - Ms. Johnson')

        # Check if the "Recent Polls" section is present
        self.assertContains(response, '<h2>Recent Polls</h2>')
        self.assertContains(response, 'Poll 1: What\'s your favorite subject?')
        self.assertContains(response, 'Poll 2: How do you rate the current semester?')

    def test_make_new_poll_button(self):
        """Test that the 'Make New Poll' button is visible on the homepage."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="make-poll-button">Make New Poll</button>')  # Check for the button

    def test_join_poll_button(self):
        """Test that the 'Join Poll' button is visible on the homepage."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="join-poll-button" type="submit">Join Poll</button>')  # Check for the button

    def test_logout_button(self):
        """Test that the 'Logout' button is visible on the homepage."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>')  # Check for the logout button

    def test_footer(self):
        """Test that the footer is visible on the homepage with correct copyright text."""
        response = self.client.get(self.url)

        self.assertContains(response, '<footer><p>&copy; 2025 Polling System</p></footer>')  # Check for the footer
