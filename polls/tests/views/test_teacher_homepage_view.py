from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TeacherHomeViewTestCase(TestCase):
    """Tests for the teacher home (dashboard) view with the page content."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('teacher_home_interface') 
        self.user = User.objects.get(username='@johndoe')

    def test_teacher_home_url(self):
        """Test that the URL is correct."""
        self.assertEqual(self.url, '/') 

    def test_get_teacher_home(self):
        """Test that the teacher homepage (dashboard) loads properly."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teacher_home_interface.html') 

        # Check for expected elements in the HTML (e.g., the title, welcome message)
        self.assertContains(response, '<h1>Home</h1>')
        self.assertContains(response, 'Welcome, Teacher!')

    def test_get_teacher_home_logged_in(self):
        """Test that logged-in teachers are not redirected (same page as both homepage and dashboard)."""
        self.client.login(username=self.user.username, password="Password123")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teacher_home_interface.html') 

    def test_teacher_home_page_contains_classes_and_polls(self):
        """Test that the teacher homepage contains the teacher's classes and polls."""
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
        """Test that the 'Make New Poll' button is on the teacher homepage."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="make-poll-button">Make New Poll</button>')

    def test_logout_button(self):
        """Test that the 'Logout' button is visible on the teacher homepage."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button class="logout-button">Logout</button>')

    def test_view_poll_results_button(self):
        """Test that the 'View Poll Results' button is visible and functional."""
        response = self.client.get(self.url)

        # Check if the 'View Poll Results' button is present
        self.assertContains(response, '<button class="btn btn-purple">View Poll Results</button>')

        # Ensure the link for the 'View Poll Results' button works (replace `poll.id` with an actual poll ID)
        poll_id = 1  # Replace with an actual poll ID you are testing for
        self.assertContains(response, f'href="/polls/{poll_id}/results/"')  # Update with the correct URL structure
