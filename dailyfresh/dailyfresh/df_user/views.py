from django.shortcuts import render
from django.http.response import HttpResponseRedirect, JsonResponse,\
    HttpResponse
from .models import *
from df_goods.models import *
from df_cart.models import *
from df_order.models import *
from hashlib import sha1
from .islogin import *

# Create your views here.
def register(request):
    context = {'title':'注册'}
    return render(request, 'df_user/register.html', context)

def register_handle(request):
    #接收用户提交的信息
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')
    
    # 判断两次输入的密码是否一致
    if upwd != ucpwd:
        return HttpResponseRedirect('/df_user/register')
    
    # 对密码原文进行sha1的加密
    # 创建sha1的对象
    s1 = sha1()
    # 对passswd进行sha1的加密
    #s1.update(passwd) # python2的写法
    s1.update(upwd.encode()) # python3的写法
    upwd2 = s1.hexdigest()
    
    # 创建对象 填入数据 然后插入数据库中
    user = userInfo()
    user.u_name = uname
    user.u_pwd = upwd2
    user.u_email = uemail
    user.save()
    
    return HttpResponseRedirect('/df_user/login')

def register_exist(request):
    #接收用户传入的unanme参数
    uname = request.GET['uname']
    
    #在数据库中查找是否存在该用户名
    count = userInfo.objects.filter(u_name=uname).count()
    return JsonResponse({'count':count})

def login(request):
    context = {'title':'登录'}
    return render(request, 'df_user/login.html', context)

def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu')
    
    users = userInfo.objects.filter(u_name = uname)
    if len(users)>=1:
        # 对密码原文进行sha1的加密
        # 创建sha1的对象
        s1 = sha1()
        # 对passswd进行sha1的加密
        #s1.update(passwd) # python2的写法
        s1.update(upwd.encode()) # python3的写法
        upwd2 = s1.hexdigest()
        
        #和数据库中的密文进行比较
        if upwd2 == users[0].u_pwd:
            url = request.COOKIES.get('url','/df_user/info')
            red = HttpResponseRedirect(url)
            
            if jizhu:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','')
            #登录成功
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            
            return red
        else:
            #登录失败 密码错误
            context = {'title':'登录','error_pwd':1,'error_name':0
                       ,'uname':uname, 'upwd':upwd}
            return render(request, 'df_user/login.html', context)
    else:
        #用户名不存在
        context = {'title':'登录','error_pwd':0,'error_name':1
                   ,'uname':uname, 'upwd':upwd}
        return render(request, 'df_user/login.html', context)
    
@islogin
def info(request):
    user_email = userInfo.objects.get(id = request.session['user_id']).u_email
    user_address = userInfo.objects.get(id = request.session['user_id']).u_address
    user_phone = userInfo.objects.get(id = request.session['user_id']).u_phone
    
    goods_ids = request.COOKIES.get('goods_ids')
    if goods_ids and goods_ids != '':
        goods_ids = goods_ids.split(',')
    else:
        goods_ids = [] 
       
    goods_list = [] 
    for id in goods_ids:
        if id != '':
            good = GoodsInfo.objects.get(id=id)
            goods_list.append(good) 
    
    context = {'title': '用户中心', 
               'user_name' : request.session['user_name'],
               'user_email' : user_email,
               'user_address': user_address,
               'user_phone': user_phone,
               'info':1,
               'page_name':1,
               'goods_list':goods_list,}
    return render(request, 'df_user/user_center_info.html',context)

@islogin
def order(request):
    uid = request.session['user_id']
    orders = OrderInfo1.objects.filter(user_id = uid,isPay = 1)
    
    context = {'title':'全部订单','order':1,'page_name':1,
               'user_name' : request.session['user_name'],
               'orders':orders}
    return render(request, 'df_user/user_center_order.html',context)

@islogin
def site(request):
    user = userInfo.objects.get(id = request.session['user_id'])
    if request.method == 'POST':
        #当用户通过表单提交信息的时候 request.method='POST' 此时获取提交过来的参数，并保存到数据库中
        post = request.POST
        user.u_shou = post.get('u_shou')
        user.u_address = post.get('u_address')
        user.u_youbian = post.get('u_youbian')
        user.u_phone = post.get('u_phone')
        user.save()
    else:
        #当用户通过url直接访问df_user/site 的时候request.method='GET' 此时无需进行任何操作，直接通过模型类获取属性即可
        pass
    
    context = {'title':'收货地址',
               'user_name' : request.session['user_name'],
               'ushou':user.u_shou,
               'uaddress':user.u_address,
               'uyoubian':user.u_youbian,
               'uphone':user.u_phone,
               'site':1,
               'page_name':1,}
    
    return render(request, 'df_user/user_center_site.html',context)

def logout(request):
    request.session.flush() #清理session缓存
    return HttpResponseRedirect('/df_user/login')
