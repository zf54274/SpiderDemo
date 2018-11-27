from django.shortcuts import render
from .models import *
from df_order.models import *
from django.http.response import JsonResponse


# Create your views here.
def cart(request):
    #从session中获取当前用户的id
    uid = request.session.get('user_id')
    
    #根据id搜索当前用户放入购物车的品种和数量
    carts = CarInfo.objects.filter(user_id = uid)
    
    context = {'title':'购物车',
               'cart_name':1,
               'carts':carts,}
    return render(request, 'df_cart/cart.html', context)

def add(request, gid, count):
    #从session中获取当前用户的id
    uid = request.session.get('user_id')
    count = int(count)
    
    carts = CarInfo.objects.filter(user_id = uid, goods_id = gid)
    if len(carts) >= 1:
        #购物车中已经有对应的商品
        cart = carts[0]
        cart.count += count
        cart.save()
    else:
        #购物车中没有对应的商品
        cart = CarInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
        cart.save()
        
    #JSON返回商品的数量
    result = CarInfo.objects.filter(user_id = uid).count()
    return JsonResponse({'count':result})

def edit(request, gid, count):
    try:
        cart = CarInfo.objects.get(id = gid)
        cart.count = int(count)
        cart.save()
        data = {'ok':0}
    except Exception as e:
        data = {'ok':1}
    return JsonResponse(data)

def delete(request, cart_id):
    try:
        cart = CarInfo.objects.get(id = cart_id)
        cart.delete()
        data = {'ok':0}
    except Exception as e:
        data = {'ok':1}
    return JsonResponse(data)
        
        
# def cart_submit(request,cart_id):
#     order_id = ""
#     for i in range(10):
#         num = str(random.randint(0,9))
#         order_id += num
#     
#     cart = CarInfo.objects.get(id = cart_id)
#     order = OrderInfo0()
#     order.order_id = order_id
#     order.isPay = 0
#     order.user_id = uid
#     order.cart_id = cart.id
#     order.save() 
#     
#     return HttpResponseRedirect('/df_order/')
