from django.db import models


class User(models.Model):
    U_id = models.AutoField(primary_key=True)
    stu_id = models.CharField(max_length=14)
    user_name = models.CharField(max_length=30)
    pwd = models.CharField(max_length=20)
    apply_time = models.DateField(auto_now_add=True)


class Question(models.Model):
    Q_id = models.AutoField(primary_key=True)
    Q_subject = models.CharField(max_length=20)
    question = models.TextField()
    option_A = models.TextField()
    option_B = models.TextField()
    option_C = models.TextField()
    option_D = models.TextField()
    q_key = models.CharField(max_length=4)


class Collection(models.Model):
    C_id = models.AutoField(primary_key=True)
    U_id = models.IntegerField()
    Q_id = models.IntegerField()
    status = models.IntegerField()


class Visit(models.Model):
    V_id = models.AutoField(primary_key=True)
    U_id = models.IntegerField()
    Q_id = models.IntegerField()
