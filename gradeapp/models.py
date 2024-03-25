from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    groups = models.ManyToManyField('auth.Group', related_name='user_set_custom')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='user_set_custom')

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    # Add any other fields relevant to your questions

    def __str__(self):
        return self.question_text

class Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.exam_name

class ScoreSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return {self.user.username}