from django.conf.urls import url
from . import views

urlpatterns = [
    url('^register$',views.register),
    url('^register_handle$',views.register_handle),
    url('^register_exist$',views.register_exist),
    url('^login$',views.login),
    url('^login_handle$',views.login_handle),
    url('^info$', views.info),
    url('^order$',views.order),
    url('^site$',views.site),
    url('^logout$',views.logout),
]