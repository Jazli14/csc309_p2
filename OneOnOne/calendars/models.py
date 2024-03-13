from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserAccount

class Calendar(models.Model):
    teacher = models.ForeignKey(UserAccount, related_name='teacher_calendars', on_delete=models.CASCADE)
    students = models.ManyToManyField(UserAccount, related_name='student_calendars')
    start_date = models.DateField()
    end_date = models.DateField()
    working_day_start = models.TimeField()
    working_day_end = models.TimeField()
    title = models.CharField(max_length=255, default="title not set")

    def __str__(self):
        return f"Calendar for {self.teacher.username}"

class TimeBlock(models.Model):
    MEETING_TYPE_CHOICES = [
        ('booked', 'Booked'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
    ]

    calendar = models.ForeignKey(Calendar, related_name='time_blocks', on_delete=models.CASCADE)
    student = models.ForeignKey(UserAccount, related_name='student_time_blocks', on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    type = models.CharField(
        max_length=10,
        choices=MEETING_TYPE_CHOICES,
        default='pending',
    )
    priority_flag = models.BooleanField(default=False)

    def __str__(self):
        return f"Meeting '{self.title}' on {self.start_time} for {self.calendar.teacher.username} and {self.student.username}"

