from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from polls.models import Class, ClassStudent, Poll, StudentQuizResult

User = get_user_model()

class StudentClassPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='teach', password='pass123', role='teacher')
        self.student = User.objects.create_user(username='stud', password='pass123', role='student')

        self.class_instance = Class.objects.create(name='Math 204', teacher=self.teacher)
        self.class_url = reverse('class_view_student', args=[self.class_instance.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.class_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url.lower())

    def test_forbidden_if_student_not_enrolled(self):
        self.client.login(username='stud', password='pass123')
        response = self.client.get(self.class_url)
        self.assertEqual(response.status_code, 403)

    def test_class_page_loads_for_enrolled_student(self):
        ClassStudent.objects.create(student=self.student, class_instance=self.class_instance)
        self.client.login(username='stud', password='pass123')

        response = self.client.get(self.class_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Math 204')

    def test_grade_and_poll_summary_displayed(self):
        ClassStudent.objects.create(student=self.student, class_instance=self.class_instance)
        self.client.login(username='stud', password='pass123')

        poll = Poll.objects.create(title='Midterm', class_instance=self.class_instance, created_by=self.teacher, is_done=True)
        StudentQuizResult.objects.create(student=self.student, poll=poll, score=3, total_questions=5)

        response = self.client.get(self.class_url)
        self.assertContains(response, 'Midterm')
        self.assertContains(response, '60')  # 3/5 = 60%

    def test_handles_no_polls_gracefully(self):
        ClassStudent.objects.create(student=self.student, class_instance=self.class_instance)
        self.client.login(username='stud', password='pass123')

        response = self.client.get(self.class_url)
        self.assertContains(response, 'No polls yet')
        self.assertContains(response, 'N/A')  # Grade and average fallback
