from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserAccount(AbstractUser):
    TEACHER = 't'
    USER = 'u'
    USER_TYPE_CHOICES = [
        (TEACHER, 'Teacher'),
        (USER, 'User'),
    ]

    user_type = models.CharField(
        max_length=1,
        choices=USER_TYPE_CHOICES,
        default=USER,
    )

class Contact(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='contacts')
    contact = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='contact_of')

    class Meta:
        unique_together = ['user', 'contact']

# class Calendar(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=200, blank=True)
#     start_date = models.DateField()
#     end_date = models.DateField()
