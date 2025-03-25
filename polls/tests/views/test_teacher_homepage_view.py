from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from polls.models import Class, Poll

User = get_user_model()

class TeacherHomeViewTests(TestCase):
    """Comprehensive tests for the teacher dashboard view."""

    @classmethod
    def setUpTestData(cls):
        cls.teacher = User.objects.create_user(
            username='teacher1', password='Password123', role='teacher'
        )
        cls.class1 = Class.objects.create(name='Math 101', teacher=cls.teacher)
        cls.class2 = Class.objects.create(name='History 202', teacher=cls.teacher)

        cls.poll1 = Poll.objects.create(title='Poll 1', description='Topic preferences', created_by=cls.teacher)
        cls.poll2 = Poll.objects.create(title='Poll 2', description='Lesson feedback', created_by=cls.teacher)

        cls.url = reverse('teacher_home_interface')
        cls.login_url = reverse('login_interface')

    def login(self):
        self.client.login(username='teacher1', password='Password123')

    def test_redirects_if_not_logged_in(self):
        """Ensure unauthenticated users are redirected to login."""
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{self.login_url}?next={self.url}")

    def test_page_loads_for_logged_in_teacher(self):
        self.login()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teacher_home_interface.html')
        self.assertContains(response, 'Your Classes')
        self.assertContains(response, 'Your Polls')
        self.assertContains(response, 'Math 101')
        self.assertContains(response, 'History 202')
        self.assertContains(response, 'Poll 1')
        self.assertContains(response, 'Poll 2')

    def test_make_new_poll_button_present(self):
        self.login()
        response = self.client.get(self.url)
        self.assertContains(response, '<button class="make-poll-button">Make New Poll</button>')

    def test_logout_button_visible(self):
        self.login()
        response = self.client.get(self.url)
        self.assertInHTML(
            '<button type="submit" class="logout-button">Logout</button>',
            response.content.decode()
        )

    def test_view_poll_results_button_links_correctly(self):
        self.login()
        response = self.client.get(self.url)

        for poll in [self.poll1, self.poll2]:
            poll_results_url = reverse("view_poll_results", args=[poll.id])
            self.assertContains(response, f'href="{poll_results_url}"')
            self.assertContains(response, "View Poll Results")

    def test_page_layout_and_footer(self):
        self.login()
        response = self.client.get(self.url)
        self.assertContains(response, "&copy; 2025 Polling System")
        self.assertContains(response, "@media screen and (max-width: 768px)")

    def test_template_context_contains_expected_data(self):
        self.login()
        response = self.client.get(self.url)
        self.assertIn("polls", response.context)
        self.assertIn("classes", response.context)
        self.assertEqual(set(response.context["polls"]), {self.poll1, self.poll2})
        self.assertEqual(set(response.context["classes"]), {self.class1, self.class2})
