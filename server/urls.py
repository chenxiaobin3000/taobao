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
from app.views.system import department, market, permission, role, user
from app.views.original import order

urlpatterns = [
    # 账号
    path('api/account/register', account.register),
    path('api/account/login', account.login),
    path('api/account/logout', account.logout),
    path('api/account/setPassword', account.setPassword),
    path('api/account/resetPwd', account.resetPwd),

    # 用户
    path('api/user/add', user.addUser),
    path('api/user/set', user.setUser),
    path('api/user/del', user.delUser),
    path('api/user/get', user.getUser),
    path('api/user/getByPhone', user.getUserByPhone),
    path('api/user/getList', user.getUserList),

    # 订单
    path('api/order/add', order.addOrder),
    path('api/order/set', order.setOrder),
    path('api/order/del', order.delOrder),
    path('api/order/get', order.getOrder),
    path('api/order/getList', order.getOrderList),

    path('', TemplateView.as_view(template_name='index.html'))
]
