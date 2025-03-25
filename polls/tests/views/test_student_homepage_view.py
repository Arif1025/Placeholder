from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from polls.models import Poll, Class, ClassStudent

User = get_user_model()

class StudentHomeViewTests(TestCase):
    """Tests for the student's homepage view."""

    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher1', password='password123', role='teacher')
        self.student = User.objects.create_user(username='johndoe', password='password123', role='student')

        # Create a class and assign it to the student
        self.class1 = Class.objects.create(name='Math 101', teacher=self.teacher)
        self.class2 = Class.objects.create(name='History 202', teacher=self.teacher)
        
        ClassStudent.objects.create(student=self.student, class_instance=self.class1)
        ClassStudent.objects.create(student=self.student, class_instance=self.class2)

        self.url = reverse('student_home_interface')
        
    def login_student(self):
        self.client.login(username='johndoe', password='password123')

    def test_homepage_loads_for_logged_in_student(self):
        self.login_student()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Ensure the classes section is displayed
        self.assertContains(response, "Your Enrolled Classes")
        self.assertContains(response, "Math 101")
        self.assertContains(response, "History 202")

        # Ensure the teacher's name is displayed
        self.assertContains(response, "Teacher: teacher1")

    def test_classes_and_teachers_displayed(self):
        self.login_student()
        response = self.client.get(self.url)
        self.assertContains(response, "Math 101")
        self.assertContains(response, "History 202")
        self.assertContains(response, self.teacher.username)

    def test_joined_polls_displayed(self):
        self.login_student()
        response = self.client.get(self.url)
        self.assertContains(response, "Poll 1")
        self.assertContains(response, "Poll 2")

    def test_action_buttons_visible(self):
        self.login_student()
        response = self.client.get(self.url)
        self.assertContains(response, "Join Poll")
        self.assertContains(response, "Logout")
        self.assertContains(response, "Back")

    def test_footer_displayed(self):
        self.login_student()
        response = self.client.get(self.url)
        self.assertContains(response, "&copy; 2025 Polling System")

    def test_mobile_responsiveness_styles(self):
        self.login_student()
        response = self.client.get(self.url)
        self.assertContains(response, "@media screen and (max-width: 768px)")

    def test_page_does_not_expose_teacher_only_features(self):
        self.login_student()
        response = self.client.get(self.url)
        self.assertNotContains(response, "Create Quiz")
        self.assertNotContains(response, "Manage Classes")
