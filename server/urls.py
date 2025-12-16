"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic.base import TemplateView
from app.views import account
from app.views.system import company, good, market, permission, role, shop, user
from app.views.original import order

urlpatterns = [
    # 账号
    path('api/account/register', account.register),
    path('api/account/login', account.login),
    path('api/account/logout', account.logout),
    path('api/account/setPassword', account.setPassword),
    path('api/account/resetPassword', account.resetPassword),

    # 用户
    path('api/user/add', user.add),
    path('api/user/set', user.set),
    path('api/user/del', user.delete),
    path('api/user/get', user.get),
    path('api/user/getByPhone', user.getByPhone),
    path('api/user/getList', user.getList),

    # 商品
    path('api/good/add', good.add),
    path('api/good/set', good.set),
    path('api/good/del', good.delete),
    path('api/good/get', good.get),
    path('api/good/getList', good.getList),
    
    # 订单
    path('api/order/add', order.add),
    path('api/order/set', order.set),
    path('api/order/del', order.delete),
    path('api/order/get', order.get),
    path('api/order/getList', order.getList),

    path('', TemplateView.as_view(template_name='index.html'))
]
