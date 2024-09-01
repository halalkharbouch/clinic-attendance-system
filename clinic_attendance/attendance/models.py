# attendance/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_staff_member = models.BooleanField(default=False)
    department = models.CharField(max_length=100, blank=True)
    staff_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.check_in_time.date()}"
    
