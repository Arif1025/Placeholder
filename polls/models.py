import uuid
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
    is_done = models.BooleanField(default=False)

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_polls')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)


class Question(models.Model):
    QUESTION_TYPES = [
        ('written', 'Written Answer'),
        ('mcq', 'Multiple Choice'),
    ]

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255) 
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='written')
    correct_answer = models.CharField(max_length=255, blank=True) # For written answers

    def __str__(self):
        return self.text

    def get_options(self):
        """Return a list of options if question_type='mcq'."""
        return self.options.split(',') if self.options else []
    


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text.strip().replace('\r\n', ' ').replace('\n', ' ')
    
    def save(self, *args, **kwargs):
        self.text = self.text.strip().replace('\r\n', ' ').replace('\n', ' ')
        super().save(*args, **kwargs)

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
    
    students = models.ManyToManyField('self', related_name='teachers', through='Teaching', symmetrical=False, blank=True)

    def __str__(self):
        return self.username

class Teaching(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teaching')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='being_taught_by')

    def __str__(self):
        return f"{self.teacher} teaches {self.student}"
    
class Class(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='classes')

    def __str__(self):
        return self.name

class ClassStudent(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.student.username} in {self.class_instance.name}"
    
class StudentResponse(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class StudentQuizResult(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    