from django.db import models

# Create your models here.
class login_detail(models.Model):
    email = models.CharField(max_length=250, primary_key=True)
    password = models.CharField(max_length=250)
    user_name = models.CharField(max_length=250)

class hobbies(models.Model):
    email = models.CharField(max_length=250, primary_key=True)
    hobbies = models.CharField(max_length=1000)
