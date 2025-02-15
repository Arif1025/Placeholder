from django.db import models
from django.contrib.auth.models import User



class Question(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=225)
    # category = models.CharField(max_length=100, blank=True)
    # difficulty_level = models.IntegerField(choices=[(1,'Easy'),(2,'Medium'),(3,'Hard')], default=1)
    # is_active = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.question_text} ({self.category}-{self.difficulty_level})'

class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # update_at = models.DateTimeField(auto_now=True)
    created_by_id = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Choice(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Response(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_id = models.ForeignKey(Choice, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user_id', 'question_id')

    def __str__(self):
        return f'{self.user.username} voted for {self.choice.choice_text}'