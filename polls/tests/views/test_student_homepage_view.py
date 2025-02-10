from django.test import TestCase
from django.urls import reverse
from tutorials.models import User


class HomeViewTestCase(TestCase):
    """Tests for the home view with the updated page content."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(username='@johndoe')

    def test_home_url(self):
        """Test that the URL is correct."""
        self.assertEqual(self.url, '/')

    def test_get_home(self):
        """Test that the homepage loads properly."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        # Check for expected elements in the HTML (e.g., the title, welcome message)
        self.assertContains(response, '<h1>Home</h1>')
        self.assertContains(response, 'Welcome, John Doe!')

    def test_get_home_logged_in(self):
        """Test that logged-in users are redirected to the dashboard."""
        self.client.login(username=self.user.username, password="Password123")

        response = self.client.get(self.url, follow=True)

        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_home_page_contains_classes_and_polls(self):
        """Test that the homepage contains the user's classes and polls."""
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
        """Test that the 'Make New Poll' button is on the homepage."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="make-poll-button">Make New Poll</button>')

    def test_logout_button(self):
        """Test that the 'Logout' button is visible."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>')
