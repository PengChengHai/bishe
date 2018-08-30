from django.db import models

# Create your models here.
class exam_status(models.Model):
    status = models.CharField(max_length=8)
    title = models.TextField(max_length=200)
    duration = models.CharField(max_length=50)
    count = models.CharField(max_length=5)
    subject = models.CharField(max_length=20)

class score(models.Model):
    stu_id = models.CharField(max_length=20)
    title = models.TextField(max_length=200)
    count = models.CharField(max_length=5)
    result = models.CharField(max_length=60)
    time = models.DateField(auto_now_add=True,editable = True)