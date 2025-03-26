from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from polls.models import Class, ClassStudent, Poll
from polls.forms import JoinPollForm

User = get_user_model()

class StudentHomePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create teacher
        self.teacher = User.objects.create_user(username='teach1', password='testpass123', role='teacher')

        # Create student and log in
        self.student = User.objects.create_user(username='stud1', password='pass123', role='student')
        self.client.login(username='stud1', password='pass123')

        # Create class and link student to it
        self.class_obj = Class.objects.create(name='Biology 101', teacher=self.teacher)
        ClassStudent.objects.create(student=self.student, class_instance=self.class_obj)

        # Create a poll and join it as the student
        self.poll = Poll.objects.create(title='Bio Quiz', created_by=self.teacher)
        self.poll.participants.add(self.student)

    def test_student_homepage_loads(self):
        url = reverse('student_home_interface')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_home_interface.html')

    def test_student_classes_are_displayed(self):
        response = self.client.get(reverse('student_home_interface'))
        self.assertContains(response, 'Biology 101')
        self.assertContains(response, self.teacher.username)

    def test_joined_polls_are_displayed(self):
        response = self.client.get(reverse('student_home_interface'))
        self.assertContains(response, 'Bio Quiz')

    def test_join_poll_button_redirect_link_exists(self):
        response = self.client.get(reverse('student_home_interface'))
        self.assertContains(response, 'Join Poll')
        self.assertContains(response, reverse('enter_poll_code'))

    def test_enter_poll_code_form_loads(self):
        response = self.client.get(reverse('enter_poll_code'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="poll_code"')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('student_home_interface'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url.lower())

    def test_enter_poll_code_form_loads(self):
        response = self.client.get(reverse('enter_poll_code'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="poll_code"')
        self.assertIsInstance(response.context['form'], JoinPollForm)

    def test_join_poll_with_valid_code(self):
        valid_code = self.poll.code
        self.client.logout()
        self.client.login(username='stud1', password='pass123')

        response = self.client.post(reverse('enter_poll_code'), {'poll_code': valid_code})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('student_home_interface'))

        self.poll.refresh_from_db()
        self.assertIn(self.student, self.poll.participants.all())

    def test_join_poll_with_invalid_code(self):
        response = self.client.post(reverse('enter_poll_code'), {'poll_code': 'INVALIDCODE'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid poll code.')

class StudentJoinClassTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a teacher and some classes
        self.teacher = User.objects.create_user(username='teacher1', password='testpass', role='teacher')
        self.class1 = Class.objects.create(name='Economics 285', teacher=self.teacher)
        self.class2 = Class.objects.create(name='History 101', teacher=self.teacher)

        # Create student and log in
        self.student = User.objects.create_user(username='student1', password='pass123', role='student')
        self.client.login(username='student1', password='pass123')

    def test_join_class_form_renders(self):
        response = self.client.get(reverse('student_home_interface'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Join a Class:')
        self.assertContains(response, 'Economics 285')
        self.assertContains(response, 'History 101')

    def test_student_can_join_class(self):
        response = self.client.post(reverse('student_home_interface'), {
            'class_choice': self.class1.id
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Economics 285')
        self.assertTrue(ClassStudent.objects.filter(student=self.student, class_instance=self.class1).exists())

    def test_joined_classes_disappear_from_dropdown(self):
        ClassStudent.objects.create(student=self.student, class_instance=self.class1)

        response = self.client.get(reverse('student_home_interface'))

        dropdown_html = response.content.decode().split('Join a Class:')[1]
        self.assertNotIn('Economics 285', dropdown_html)
        self.assertIn('History 101', dropdown_html)

    def test_student_added_to_poll_participants_on_join(self):
        poll = Poll.objects.create(title='Econ Quiz', class_instance=self.class1, created_by=self.teacher, is_done=False)

        self.client.post(reverse('student_home_interface'), {
            'class_choice': self.class1.id
        }, follow=True)

        poll.refresh_from_db()
        self.assertIn(self.student, poll.participants.all())

