from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$',views.order),
#     url('^order_handle/(\d+)$',views.order_handle)
]