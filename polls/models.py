from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return self.choice_text

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.question} - {self.choice}"


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('professor', 'Professor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Written Answer'),
        ('mcq', 'Multiple Choice'),
    ]

    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    options = models.TextField(blank=True, help_text="Comma-separated options for MCQ")

    def get_options(self):
        return self.options.split(',') if self.options else []