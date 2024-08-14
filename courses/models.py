from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class CourseCategory(models.Model):
    name = models.CharField(max_length=10,blank=False,null=False)
    icon = models.ImageField(upload_to='icons/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       ordering=('-created_at',)

    def __str__(self):
        return self.name


class Course(models.Model):
    user = models.ForeignKey(User, related_name="courses", on_delete=models.CASCADE)
    category = models.ForeignKey(CourseCategory, related_name="courses", on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=False,null=False)
    desc = models.TextField (blank=False,null=False)
    price = models.DecimalField(decimal_places=2, max_digits=10,blank=False,null=False)
    video = models.FileField(upload_to='videos/',blank=True,null=True)
    image = models.ImageField(upload_to='images/', blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name