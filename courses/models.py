from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User 
User = get_user_model()

class CourseCategory(models.Model):
    name = models.CharField(max_length=10,blank=False,null=False)
    image = models.ImageField(upload_to='icons/', blank=True,null=True)
    #des=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
       ordering=('-created_at',)

    def __str__(self):
        return self.name
    

class DiscountCourse(models.Model):
    name = models.CharField(max_length=200,blank=False,null=False)
    desc = models.TextField (blank=False,null=False)
    TYPE_CHOICES=(
        ('درصدی','درصدی'),
        ('مقدار','مقدار'),
    )
    type=models.CharField(max_length=10,choices=TYPE_CHOICES,default='درصدی')
    value = models.IntegerField(primary_key=True,default=1)
    is_active=models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    expired_date=models.DateTimeField()

    class Meta:
        ordering = ("-created_at",)
    
    def __str__(self):
        return self.name




class Course(models.Model):
    user = models.ForeignKey(User, related_name="courses", on_delete=models.CASCADE)
    category = models.ForeignKey(CourseCategory, related_name="courses", on_delete=models.CASCADE)
    discount=models.ForeignKey(DiscountCourse,related_name='courses',on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=False,null=False)
    desc = models.TextField (blank=False,null=False)
    price = models.DecimalField(decimal_places=2, max_digits=10,blank=False,null=False)
    # video_type=
    #SKU
    video = models.FileField(upload_to='videos/',blank=True,null=True)
    image = models.ImageField(upload_to='images/', blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
    
