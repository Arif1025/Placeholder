from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from polls.models import Class, ClassStudent, Poll, StudentQuizResult

User = get_user_model()

class TeacherClassPageViewTests(TestCase):
    """Comprehensive tests for the teacher's class page view."""

    @classmethod
    def setUpTestData(cls):
        cls.teacher = User.objects.create_user(username="mrsmith", password="password123", role="teacher")
        cls.student1 = User.objects.create_user(username="john", password="password123", role="student")
        cls.student2 = User.objects.create_user(username="jane", password="password123", role="student")

        cls.class_instance = Class.objects.create(name="Math 101", teacher=cls.teacher)
        ClassStudent.objects.create(student=cls.student1, class_instance=cls.class_instance)
        ClassStudent.objects.create(student=cls.student2, class_instance=cls.class_instance)

        cls.poll = Poll.objects.create(title="Poll 1", created_by=cls.teacher, is_done=True)
        cls.poll.participants.set([cls.student1, cls.student2])

        StudentQuizResult.objects.create(student=cls.student1, poll=cls.poll, score=8, total_questions=10)
        StudentQuizResult.objects.create(student=cls.student2, poll=cls.poll, score=9, total_questions=10)

        cls.url = reverse("class_view_teacher", args=[cls.class_instance.id])
        cls.login_url = reverse("login_interface")

    def login(self):
        self.client.login(username="mrsmith", password="password123")

    def test_redirects_if_not_logged_in(self):
        """Should redirect unauthenticated users to login page."""
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{self.login_url}?next={self.url}")

    def test_404_on_invalid_class_id(self):
        """Should return 404 for a non-existent class."""
        self.login()
        invalid_url = reverse("class_view_teacher", args=[9999])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)

    def test_template_used_and_class_info_rendered(self):
        self.login()
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "class_template_page_teacher.html")
        self.assertContains(response, "Math 101")
        self.assertContains(response, f"Teacher: {self.teacher.username}")

    def test_enrolled_students_and_scores_shown(self):
        self.login()
        response = self.client.get(self.url)

        for student, score in [(self.student1, 8), (self.student2, 9)]:
            with self.subTest(student=student.username):
                self.assertContains(response, student.username)
                self.assertContains(response, f"Score: {score} / 10")

    def test_poll_list_displayed(self):
        self.login()
        response = self.client.get(self.url)
        self.assertContains(response, self.poll.title)

    def test_poll_link_and_context_binding(self):
        """Ensure poll shows up correctly and is in context."""
        self.login()
        response = self.client.get(self.url)
        self.assertIn("class", response.context)
        self.assertEqual(response.context["class"].id, self.class_instance.id)

    def test_average_grade_displayed_correctly(self):
        self.login()
        response = self.client.get(self.url)
        self.assertContains(response, "Average Grade")
        self.assertContains(response, "85")  # Avg of 80 and 90

    def test_navigation_buttons_present(self):
        self.login()
        response = self.client.get(self.url)
        self.assertContains(response, 'class="logout-button"')
        self.assertContains(response, 'class="back-button"')

    def test_footer_and_mobile_styles_exist(self):
        self.login()
        response = self.client.get(self.url)
        self.assertContains(response, "&copy; 2025 Polling System")
        self.assertContains(response, "@media screen and (max-width: 768px)")

    def test_layout_styles_applied(self):
        self.login()
        response = self.client.get(self.url)
        self.assertContains(response, "position: fixed; top: 20px; right: 20px;")
        self.assertContains(response, "position: fixed; top: 20px; left: 20px;")
