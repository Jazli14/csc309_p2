from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserAccount

class Calendar(models.Model):
    teacher = models.ForeignKey(UserAccount, related_name='teacher_calendars', on_delete=models.CASCADE)
    student = models.ForeignKey(UserAccount, related_name='student_calendars', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    working_day_start = models.TimeField()
    working_day_end = models.TimeField()
    
    def __str__(self):
        return f"Calendar for {self.teacher.username}"
