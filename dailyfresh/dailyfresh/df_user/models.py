from django.db import models

# Create your models here.
class userInfo(models.Model):
    u_name = models.CharField(max_length = 20)
    u_pwd = models.CharField(max_length = 40)
    u_email = models.CharField(max_length = 30)
    u_shou = models.CharField(max_length = 30, default='')
    u_address = models.CharField(max_length = 100, default='')
    u_youbian = models.CharField(max_length = 6, default='')
    u_phone = models.CharField(max_length = 11, default='')