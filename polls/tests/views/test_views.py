from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse
from polls.models import Poll, Question
from django.shortcuts import redirect



class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="teacheruser", password="StrongPass123")
        self.poll = Poll.objects.create(title="Test Poll", description="Poll description", created_by=self.user)
        self.question = Question.objects.create(question_text="Test Question", poll=self.poll)

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, this is the index view.")
    
    def test_homepage_view(self):
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello! This is the homepage at the root URL.")
    
    def test_register_teacher_view(self):
        response = self.client.post(reverse("register_teacher"), {
            "username": "newteacher",
            "email": "newteacher@example.com",
            "password1": "TestPass123",
            "password2": "TestPass123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newteacher").exists())
    
    def test_login_teacher_view(self):
        response = self.client.post(reverse("login_teacher"), {
            "username": "teacheruser",
            "password": "StrongPass123"
        })
        self.assertEqual(response.status_code, 302)
    
    def test_logout_teacher_view(self):
        self.client.login(username="teacheruser", password="StrongPass123")
        response = self.client.get(reverse("logout_teacher"))
        self.assertEqual(response.status_code, 302)
    
    def test_poll_list_view(self):
        response = self.client.get(reverse("poll_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Poll")
    
    def test_create_poll_view(self):
        self.client.login(username="teacheruser", password="StrongPass123")
        response = self.client.post(reverse("create_poll"), {"title": "New Poll", "description": "New poll description"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Poll.objects.filter(title="New Poll").exists())
    
    def test_delete_poll_view(self):
        self.client.login(username="teacheruser", password="StrongPass123")
        response = self.client.post(reverse("delete_poll", args=[self.poll.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Poll.objects.filter(id=self.poll.id).exists())
    
    def test_create_question_view(self):
        self.client.login(username="teacheruser", password="StrongPass123")
        response = self.client.post(reverse("create_question", args=[self.poll.id]), {"question_text": "New Question"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Question.objects.filter(question_text="New Question").exists())
    
    def test_delete_question_view(self):
        self.client.login(username="teacheruser", password="StrongPass123")
        response = self.client.post(reverse("delete_question", args=[self.question.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Question.objects.filter(id=self.question.id).exists())
