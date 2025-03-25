import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import re

# Poll model to store poll details
class Poll(models.Model):
    title = models.CharField(max_length=200)  # Title of the poll
    description = models.TextField(blank=True)  # Optional description for the poll
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # User who created the poll
        on_delete=models.CASCADE  # Deletes the poll when the user is deleted
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation

    code = models.CharField(max_length=100, blank=True, null=True)  
    is_done = models.BooleanField(default=False)  # Whether the poll is completed

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_polls')  # Users who joined the poll

    class_instance = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='polls', null=True, blank=True)

    def __str__(self):
        return self.title  # String representation of the poll (just the title)

    def save(self, *args, **kwargs):
        if not self.pk and not self.code:  # only generate code on creation
            self.code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)


# Question model to store questions related to a poll
class Question(models.Model):
    QUESTION_TYPES = [
        ('written', 'Written Answer'),
        ('mcq', 'Multiple Choice'),
    ]

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')  # Related poll
    text = models.CharField(max_length=255)  # Text of the question
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='written')  # Question type
    correct_answer = models.CharField(max_length=255, blank=True)  # Correct answer (for written answers)

    def __str__(self):
        return self.text  # String representation of the question text

    def get_options(self):
        """Return options if the question type is 'mcq'."""
        return self.options.split(',') if self.options else []


# Choice model for storing choices for multiple choice questions
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')  # Related question
    text = models.CharField(max_length=255)  # Choice text
    is_correct = models.BooleanField(default=False)  # Boolean to identify if the choice is correct

    def __str__(self):
        return self.text.strip().replace('\r\n', ' ').replace('\n', ' ')  # Return choice text cleaned of newlines

    def save(self, *args, **kwargs):
        cleaned_text = self.text.strip().replace('\r\n', ' ').replace('\n', ' ')
        self.text = re.sub(r'\s+', ' ', cleaned_text)  # Collapse multiple spaces
        super().save(*args, **kwargs)


# Custom user model extending AbstractUser to include role-based functionality
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]

    is_teacher = models.BooleanField(default=False)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')  # Role of the user

    students = models.ManyToManyField('self', related_name='teachers', through='Teaching', symmetrical=False, blank=True)  # Many-to-many relationship for teacher-student

    def __str__(self):
        return self.username  # Return the username for this user


# Teaching model to link teachers with their students
class Teaching(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teaching')  # Teacher
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='being_taught_by')  # Student

    def __str__(self):
        return f"{self.teacher} teaches {self.student}"  # String representation of teaching relationship


# Class model to represent different classes taught by a teacher
class Class(models.Model):
    name = models.CharField(max_length=255)  # Class name
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='classes')  # Teacher for this class

    def __str__(self):
        return self.name  # Return class name


# ClassStudent model to link students with specific classes
class ClassStudent(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Student
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)  # Class instance

    def __str__(self):
        return f"{self.student.username} in {self.class_instance.name}"  # Represent the class-student relationship


# StudentResponse model to store student responses for questions
class StudentResponse(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Student who provided the response
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Question being answered
    response = models.TextField()  # Student's response
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the response was submitted


# StudentQuizResult model to store the quiz results for each student
class StudentQuizResult(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Student who took the quiz
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)  # Poll (quiz) associated with the result
    score = models.IntegerField()  # Score the student achieved
    total_questions = models.IntegerField()  # Total questions in the quiz
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the result was submitted
