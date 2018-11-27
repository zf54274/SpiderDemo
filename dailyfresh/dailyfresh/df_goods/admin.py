from django.contrib import admin
from .models import *
# Register your models here.
class TypeInfoAdmin(admin.ModelAdmin):
    pass

class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id','gtitle','gprice','gunit','gkucun'
                    ,'gjianjie','gcontent','gtype']
    list_per_page = 15

admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)