from django.test import TestCase
from django.urls import reverse
from polls.models import Poll, Question, Choice
from django.contrib.auth import get_user_model

User = get_user_model()

class PollResultsPageViewTestCase(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher1', password='pass1234', is_teacher=True)
        self.client.login(username='teacher1', password='pass1234')

        self.poll = Poll.objects.create(title="Poll 1", creator=self.teacher)
        self.url = reverse('poll_results_chart', args=[self.poll.id])

    def test_poll_results_page_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_poll_results_page(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Poll Results")

    def test_back_button(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<a href="/polls/teacher_home_interface/" class="back-button">Back</a>', html=True)

    def test_download_button_present(self):
        response = self.client.get(self.url)
        download_link = f'/polls/export_poll_responses/{self.poll.id}/'
        self.assertContains(response, f'<a href="{download_link}">')
        self.assertContains(response, 'Download Report')

    def test_logout_button_present(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>', html=True)

    def test_canvas_tags_not_rendered_if_no_data(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, '<canvas id="pollChart1">')  # Because JS doesn’t render this server-side

    def test_chart_js_included(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'https://cdn.jsdelivr.net/npm/chart.js')

    def test_page_elements_styles(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'background-color: #e3f2fd')  # from body style
        self.assertContains(response, '.download-button:hover')
        self.assertContains(response, '.back-button:hover')
        self.assertContains(response, '.logout-button:hover')

    def test_footer_present(self):
        response = self.client.get(self.url)
        self.assertContains(response, "&copy; 2025 Polling System")

    def test_main_title_rendered(self):
        response = self.client.get(self.url)
        self.assertContains(response, "<h1>Poll Results</h1>", html=True)
