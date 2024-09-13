# from django.db import models
# from users.models import UserAccount
#
#
# class Top_Teachers(models.Model):
#     teacher = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=30, unique=True)
#     birth = models.CharField(max_length=10)
#     subject = models.CharField(max_length=10)
#     about = models.TextField()
#
#     class Meta:
#         ordering = ['birth', ]
#
#     def __str__(self):
#         return self.full_name
#
#
# class Top_Students(models.Model):
#     student = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=30)
#     birth = models.CharField(max_length=10)
#     major = models.CharField(max_length=10)
#     record = models.PositiveIntegerField()
#     about = models.TextField()
#
#     class Meta:
#         ordering = ['record', ]
#
#     def __str__(self):
#         return self.record
#
#
# class Tajrobi_Top_Levels(models.Model):
#     student = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=30)
#     birth = models.CharField(max_length=10)
#     major = models.CharField(max_length=10)
#     record = models.PositiveIntegerField()
#     about = models.TextField()
#
#
# class Riazi_Top_Levels(models.Model):
#     student = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=30)
#     birth = models.CharField(max_length=10)
#     major = models.CharField(max_length=10)
#     record = models.PositiveIntegerField()
#     about = models.TextField()
#
#
# class Enasani_Top_Levels(models.Model):
#     student = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=30)
#     birth = models.CharField(max_length=10)
#     major = models.CharField(max_length=10)
#     record = models.PositiveIntegerField()
#     about = models.TextField()
#
#
# class Prizes(models.Model):
#     subject = models.CharField(max_length=50)
#     about = models.CharField(max_length=200)
#     time = models.TimeField(auto_created=True)
#     image = models.ImageField()
#
#
# class Obligations(models.Model):
#     title = models.CharField(max_length=20)
#     about = models.TextField()
#     image = models.ImageField()
