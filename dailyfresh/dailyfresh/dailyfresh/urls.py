"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('df_user/',include('df_user.urls',namespace='df_user')),
    url('tinymce/', include('tinymce.urls', namespace='tinymce')),
    url('df_goods/',include('df_goods.urls',namespace='df_goods')),
    url('df_cart/',include('df_cart.urls',namespace='df_cart')),
    url('df_order/',include('df_order.urls',namespace='df_order')),
]
