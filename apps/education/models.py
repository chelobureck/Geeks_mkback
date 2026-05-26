from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='teaching_groups',
        limit_choices_to={'role': 'TEACHER'}
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='enrolled_groups',
        limit_choices_to={'role': 'STUDENT'}
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return self.name

class Schedule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='schedules')
    subject = models.CharField(max_length=255)
    day_of_week = models.CharField(max_length=20, choices=(
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    ))
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.group.name} - {self.subject} ({self.day_of_week})"

class Grade(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='grades',
        limit_choices_to={'role': 'STUDENT'}
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        limit_choices_to={'role': 'TEACHER'}
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='grades')
    value = models.IntegerField()
    comment = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.email} - {self.value}"
