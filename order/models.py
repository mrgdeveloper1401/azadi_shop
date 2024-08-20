from django.db import models
from users.models import UserAccount
from courses.models import Course


class Order(models.Model):
    user=models.ForeignKey(UserAccount,related_name='orders',on_delete=models.CASCADE)
    course=models.ManyToManyField(Course,related_name='orders')
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    
         