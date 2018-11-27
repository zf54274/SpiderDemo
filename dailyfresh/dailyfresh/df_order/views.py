from django.shortcuts import render
from df_cart.models import *
from df_user.models import *
from .models import *
from django.http.response import HttpResponseRedirect
import random

# Create your views here.
def order(request):
    uid = request.session.get('user_id')
    orders = OrderInfo1.objects.filter(user_id = uid,isPay = 0)
    user = userInfo.objects.get(id = uid)
    
    context = {'title':'提交订单',
               'order_name':1,
               'orders':orders,'user':user}
    return render(request, 'df_order/place_order.html',context)


# def order_handle(request,uid):
#     order_id = ""
#     for i in range(10):
#         num = str(random.randint(0,9))
#         order_id += num
#     
#     carts = CarInfo.objects.filter(user_id = uid)
#     for cart in carts:
#         order = OrderInfo1()
#         order.order_id = order_id
#         order.isPay = 1
#         order.user_id = uid
#         order.cart_id = cart.id
#         order.save() 
#     
#     return HttpResponseRedirect('/df_goods/')