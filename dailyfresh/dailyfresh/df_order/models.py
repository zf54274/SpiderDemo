from django.db import models

# Create your models here.
class OrderInfo1(models.Model):
    order_id = models.CharField(max_length = 10)
    user = models.ForeignKey('df_user.userInfo')
    cart = models.ForeignKey('df_cart.CarInfo')
    isPay = models.BooleanField(default = False)
    
class OrderInfo0(models.Model):
    order_id = models.CharField(max_length = 10)
    user = models.ForeignKey('df_user.userInfo')
    cart = models.ForeignKey('df_cart.CarInfo')
    isPay = models.BooleanField(default = False)