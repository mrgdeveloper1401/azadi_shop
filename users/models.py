from django.db import models
from django.contrib.auth.models import User,AbstractUser,PermissionsMixin
from django.conf import settings
from django.utils.crypto import get_random_string
import datetime
from django.utils import timezone
# Create your models here.
class Account(AbstractUser):      
      security_code = models.CharField(max_length=6,blank=True,null=True)
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
      
      def generate_security_code(self):
        """
        Returns a unique random `security_code` for given `TOKEN_LENGTH` in the settings.
        Default token length = 6
        """
        token_length = getattr(settings, "TOKEN_LENGTH", 6)
        return get_random_string(token_length, allowed_chars="0123456789")

      def is_security_code_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            minutes=settings.TOKEN_EXPIRE_MINUTES
        )
        return expiration_date <= timezone.now()

      def send_confirmation(self):
        twilio_account_sid = settings.TWILIO_ACCOUNT_SID
        twilio_auth_token = settings.TWILIO_AUTH_TOKEN
        twilio_phone_number = settings.TWILIO_PHONE_NUMBER

        self.security_code = self.generate_security_code()