from django.db import models
from django.contrib.auth.models import User,AbstractUser,PermissionsMixin
from django.conf import settings
from django.utils.crypto import get_random_string
import datetime
from django.utils import timezone
# Create your models here.
class Account(AbstractUser):      
      is_verified = models.BooleanField(default=False)
      GRADE_CHOICES=(
        ('دهم','دهم'),
        ('یازدهم','یازدهم'),
        ('دوازدهم','دوازدهم')
      
    )
      MAJOR_CHOICES=(
        ('تجربی','تجربی'),
        ('ریاضی','ریاضی'),
        ('انسانی','انسانی')
      
    )
      grade=models.CharField(max_length=10,choices=GRADE_CHOICES,default='دهم')
      major=models.CharField(max_length=10,choices=MAJOR_CHOICES,default='تجربی')
      created_at = models.DateTimeField(auto_now_add=True)
      objects = models.Manager()

      class Meta:
        ordering = ("-created_at",)

      def __str__(self):
        return self.first_name + self.last_name
      