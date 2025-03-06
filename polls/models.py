from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Written Answer'),
        ('mcq', 'Multiple Choice'),
    ]

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField() 
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='text')
    options = models.TextField(blank=True, help_text="Comma-separated options for MCQ")

    def __str__(self):
        return self.text

    def get_options(self):
        """Return a list of options if question_type='mcq'."""
        return self.options.split(',') if self.options else []
    


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return self.choice_text
    

class Response(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.question} - {self.choice}"



class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} - {self.role}"
