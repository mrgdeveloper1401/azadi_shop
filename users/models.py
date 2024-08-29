from django.db import models
from django.contrib.auth.models import User,AbstractUser,PermissionsMixin
from django.conf import settings
from django.utils.crypto import get_random_string
import datetime
from django.utils import timezone
# Create your models here.


class UserAccount(AbstractUser):
    is_verified=models.BooleanField(default=False)

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return self.username




class UserInfo (models.Model):      
      
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
    user_id=models.OneToOneField(UserAccount,on_delete=models.CASCADE)
    grade=models.CharField(max_length=10,choices=GRADE_CHOICES,default='دهم')
    major=models.CharField(max_length=10,choices=MAJOR_CHOICES,default='تجربی')
    objects = models.Manager()

    class Meta:
        ordering = ['user_id__date_joined']

    def __str__(self):
        return self.username


class Otp (models.Model) :
      
    user=models.OneToOneField(UserAccount,on_delete=models.CASCADE)
    code=models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.user.username

    def is_expired(self):
            # OTP expires after 1 minute
            return timezone.now() > self.created_at + timezone.timedelta(minutes=5)
     
        


class PasswordOtp (models.Model) :
      
    user=models.OneToOneField(UserAccount,on_delete=models.CASCADE)
    code=models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.user.username

    def is_expired(self):
            # OTP expires after 1 minute
            return timezone.now() > self.created_at + timezone.timedelta(minutes=5)
      