from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from polls.models import Class, ClassStudent, Poll, Question, StudentQuizResult

User = get_user_model()

class TeacherClassPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create teacher and login
        self.teacher = User.objects.create_user(username='teach1', password='pass123', role='teacher')
        self.client.login(username='teach1', password='pass123')

        # Create class and students
        self.class_instance = Class.objects.create(name='History 101', teacher=self.teacher)

        self.student1 = User.objects.create_user(username='student1', password='pass123', role='student')
        self.student2 = User.objects.create_user(username='student2', password='pass123', role='student')

        ClassStudent.objects.create(student=self.student1, class_instance=self.class_instance)
        ClassStudent.objects.create(student=self.student2, class_instance=self.class_instance)

        # Create a poll for the class
        self.poll = Poll.objects.create(title='History Quiz', created_by=self.teacher, class_instance=self.class_instance)

        # Add quiz results
        StudentQuizResult.objects.create(student=self.student1, poll=self.poll, score=8, total_questions=10)
        StudentQuizResult.objects.create(student=self.student2, poll=self.poll, score=6, total_questions=10)

    def test_teacher_can_view_class_page(self):
        url = reverse('class_view_teacher', args=[self.class_instance.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'class_template_page_teacher.html')
        self.assertContains(response, 'History 101')
        self.assertContains(response, 'student1')
        self.assertContains(response, 'student2')
        self.assertContains(response, 'History Quiz')

    def test_average_grade_calculation(self):
        url = reverse('class_view_teacher', args=[self.class_instance.id])
        response = self.client.get(url)

        expected_avg = round((8 + 6) / 2, 1)
        self.assertContains(response, str(expected_avg))

    def test_blocked_if_not_teacher(self):
        self.client.logout()
        self.client.login(username='student1', password='pass123')

        url = reverse('class_view_teacher', args=[self.class_instance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_view_with_no_students(self):
        empty_class = Class.objects.create(name='Empty Class', teacher=self.teacher)
        url = reverse('class_view_teacher', args=[empty_class.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Empty Class')
        self.assertNotContains(response, 'student1') 

    def test_view_with_student_but_no_results(self):
        student3 = User.objects.create_user(username='student3', password='pass123', role='student')
        ClassStudent.objects.create(student=student3, class_instance=self.class_instance)

        url = reverse('class_view_teacher', args=[self.class_instance.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'student3')
        self.assertContains(response, 'N/A')  

    def test_recent_poll_is_displayed(self):
        Poll.objects.create(title='Old Quiz', created_by=self.teacher, class_instance=self.class_instance)
        Poll.objects.create(title='Newer History Quiz', created_by=self.teacher, class_instance=self.class_instance)

        url = reverse('class_view_teacher', args=[self.class_instance.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Newer History Quiz') 

    def test_student_score_percentages(self):
        url = reverse('class_view_teacher', args=[self.class_instance.id])
        response = self.client.get(url)

        percentage1 = round((8 / 10) * 100)
        percentage2 = round((6 / 10) * 100)

        self.assertContains(response, str(percentage1))
        self.assertContains(response, str(percentage2))

    def test_class_with_no_students(self):
        empty_class = Class.objects.create(name="Empty Class", teacher=self.teacher)
        url = reverse("class_view_teacher", args=[empty_class.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enrolled Students")

    def test_student_with_zero_poll_answers(self):
        student4 = User.objects.create_user(username='student4', password='pass123', role='student')
        ClassStudent.objects.create(student=student4, class_instance=self.class_instance)

        url = reverse("class_view_teacher", args=[self.class_instance.id])
        response = self.client.get(url)
        self.assertContains(response, "student4")
        self.assertContains(response, "Grade: N/A")
        self.assertContains(response, "Polls Answered: 0")

    def test_multiple_students_some_with_no_responses(self):
        student3 = User.objects.create_user(username="student3", password="pass123", role="student")
        ClassStudent.objects.create(student=student3, class_instance=self.class_instance)

        poll = Poll.objects.create(title="Test Quiz", created_by=self.teacher, class_instance=self.class_instance)
        Question.objects.create(poll=poll, text="Q1", question_type="written", correct_answer="A")
        StudentQuizResult.objects.create(student=self.student1, poll=poll, score=1, total_questions=1)

        url = reverse("class_view_teacher", args=[self.class_instance.id])
        response = self.client.get(url)
        self.assertContains(response, "student3")
        self.assertContains(response, "Grade: N/A")

    def test_no_polls_in_class(self):
        empty_class = Class.objects.create(name="New Class", teacher=self.teacher)
        url = reverse("class_view_teacher", args=[empty_class.id])
        response = self.client.get(url)
        self.assertContains(response, "Most Recent Poll")
        self.assertContains(response, "Average Grade for Recent Poll: N/A")

    def test_all_students_have_wrong_answers(self):
        poll = Poll.objects.create(title="Wrong Answers Quiz", created_by=self.teacher, class_instance=self.class_instance)
        Question.objects.create(poll=poll, text="Q1", question_type="written", correct_answer="A")
        StudentQuizResult.objects.create(student=self.student1, poll=poll, score=0, total_questions=1)
        StudentQuizResult.objects.create(student=self.student2, poll=poll, score=0, total_questions=1)

        url = reverse("class_view_teacher", args=[self.class_instance.id])
        response = self.client.get(url)
        self.assertContains(response, "0.0")

    def test_poll_with_no_questions(self):
        Poll.objects.create(title="Empty Poll", created_by=self.teacher, class_instance=self.class_instance)
        url = reverse("class_view_teacher", args=[self.class_instance.id])
        response = self.client.get(url)
        self.assertContains(response, "Empty Poll")

    def test_student_responses_with_incomplete_data(self):
        poll = Poll.objects.create(title="Incomplete Data Quiz", created_by=self.teacher, class_instance=self.class_instance)
        StudentQuizResult.objects.create(student=self.student1, poll=poll, score=0, total_questions=0)

        url = reverse("class_view_teacher", args=[self.class_instance.id])
        response = self.client.get(url)
        self.assertContains(response, "0.0")

    def test_view_fails_for_non_teacher_user(self):
        student = User.objects.create_user(username="studentX", password="pass123", role="student")
        self.client.logout()
        self.client.login(username="studentX", password="pass123")
        url = reverse("class_view_teacher", args=[self.class_instance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_view_fails_for_teacher_not_owning_class(self):
        other_teacher = User.objects.create_user(username="other", password="pass123", role="teacher")
        self.client.logout()
        self.client.login(username="other", password="pass123")
        url = reverse("class_view_teacher", args=[self.class_instance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
