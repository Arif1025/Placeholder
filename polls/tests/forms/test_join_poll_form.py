from django.test import TestCase
from polls.forms import JoinClassForm
from polls.models import Class, CustomUser

class JoinClassFormTest(TestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.create_user(username='teacher1', password='pass123', role='teacher')
        self.class_obj = Class.objects.create(name='Art 201', teacher=self.teacher)

    def test_form_valid_with_existing_class(self):
        form = JoinClassForm(data={'class_choice': self.class_obj.id})
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_blank(self):
        form = JoinClassForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('class_choice', form.errors)

    def test_form_invalid_with_nonexistent_class(self):
        form = JoinClassForm(data={'class_choice': 999})
        self.assertFalse(form.is_valid())
        self.assertIn('class_choice', form.errors)
