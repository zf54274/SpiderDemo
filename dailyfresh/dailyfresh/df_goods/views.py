from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    fruit = GoodsInfo.objects.filter(gtype_id=1).order_by('-id')[:4] # 最新产品
    fruit2 = GoodsInfo.objects.filter(gtype_id=1).order_by('-gclick')[:3] # 热销产品
    fish = GoodsInfo.objects.filter(gtype_id=2).order_by('-id')[:4] # 最新产品
    fish2 = GoodsInfo.objects.filter(gtype_id=2).order_by('-gclick')[:3] # 热销产品
    meat = GoodsInfo.objects.filter(gtype_id=3).order_by('-id')[:4] # 最新产品
    meat2 = GoodsInfo.objects.filter(gtype_id=3).order_by('-gclick')[:3] # 热销产品
    egg = GoodsInfo.objects.filter(gtype_id=4).order_by('-id')[:4] # 最新产品
    egg2 = GoodsInfo.objects.filter(gtype_id=4).order_by('-gclick')[:3] # 热销产品
    vegetable = GoodsInfo.objects.filter(gtype_id=5).order_by('-id')[:4] # 最新产品
    vegetable2 = GoodsInfo.objects.filter(gtype_id=5).order_by('-gclick')[:3] # 热销产品
    frozen = GoodsInfo.objects.filter(gtype_id=6).order_by('-id')[:4] # 最新产品
    frozen2 = GoodsInfo.objects.filter(gtype_id=6).order_by('-gclick')[:3] # 热销产品
    
    context = {'title':'首页',
               'fruit':fruit, 'fruit2':fruit2,
               'fish':fish, 'fish2':fish2,
               'meat':meat, 'meat2':meat2,
               'egg':egg, 'egg2':egg2,
               'vegetable':vegetable, 'vegetable2':vegetable2,
               'frozen':frozen, 'frozen2':frozen2,
               'guest_cart':1}
    return render(request, 'df_goods/index.html', context)

def goodlist(request, typeid, pageid, sort):
    goodtype = TypeInfo.objects.get(id = typeid)
    #获取最新发布的商品
    newgood = GoodsInfo.objects.filter(gtype_id = typeid).order_by('-id')[:2]
    #所有产品的默认排序
    if sort == '1':
        sumGoodlist = GoodsInfo.objects.filter(gtype_id = typeid).order_by('-id')
    #价格排序
    elif sort == '2':
        sumGoodlist =  GoodsInfo.objects.filter(gtype_id = typeid).order_by('gprice')
    #人气排序
    elif sort == '3':
        sumGoodlist =  GoodsInfo.objects.filter(gtype_id = typeid).order_by('-gclick')
    #分页
    paginator = Paginator(sumGoodlist,15)     
    goodList = paginator.page(int(pageid))
    
    page_num = paginator.page_range
    
    
    context = {'title':'商品列表',
               'guest_cart':1,
               'newgood':newgood,
               'goodList':goodList,'goodtype':goodtype,
               'typeid':typeid,'pageid':int(pageid),'sort':sort,
               'page_num':page_num,}
    return render(request, 'df_goods/list.html', context)

def detail(request,id):
    #获取类型id
    typeid = GoodsInfo.objects.get(id = id).gtype_id
    #获取产品类型
    goodtype = TypeInfo.objects.get(id = typeid)
    #获取商品的对象
    good = GoodsInfo.objects.get(id = id)
    #增加点击量
    good.gclick = good.gclick + 1
    good.save()
    #获取最新发布的商品
    newgood = GoodsInfo.objects.filter(gtype_id = typeid).order_by('-id')[:2]
    
    context = {'title':'商品详情',
               'guest_cart':1,
               'detail':1,'typeid':typeid,
               'newgood':newgood,'goodtype':goodtype,
               'g':good,}
    response = render(request, 'df_goods/detail.html', context)
    
    #读取请求的Cookies
    goods_ids = request.COOKIES.get('goods_ids')
    #判断cookies中的商品id序列是否为空
    
    if goods_ids and goods_ids != '':
        #不为空 以逗号进行分割 把字符串转换成列表
        goods_ids = goods_ids.split(',')
        #如果列表中已经有当前的id则需要移除
        if id in goods_ids:
            goods_ids.remove(id)
        #把当前的id放到列表的前面
        goods_ids.insert(0,id)
        #如果超过5个，则值保留前五个
        if len(goods_ids) > 5:
            goods_ids = goods_ids[0:5]
    else:
        #为空
        goods_ids = id
        
    print(goods_ids)
    #把列表重新拼接成字符串
    goods_ids = ','.join(goods_ids)
    
    response.set_cookie('goods_ids', goods_ids)
    
    return response