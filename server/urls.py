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
from app.views.system import company, good, market, permission, role, shop, user, user_shop
from app.views.original import order

urlpatterns = [
    # 账号
    path('api/account/register', account.register),
    path('api/account/login', account.login),
    path('api/account/logout', account.logout),
    path('api/account/setPassword', account.setPassword),
    path('api/account/resetPassword', account.resetPassword),

    # 公司
    path('api/company/add', company.add),
    path('api/company/set', company.set),
    path('api/company/del', company.delete),
    path('api/company/get', company.get),
    path('api/company/getList', company.getList),

    # 商品
    path('api/good/add', good.add),
    path('api/good/addList', good.addList),
    path('api/good/set', good.set),
    path('api/good/del', good.delete),
    path('api/good/get', good.get),
    path('api/good/getList', good.getList),

    # 平台
    path('api/market/add', market.add),
    path('api/market/set', market.set),
    path('api/market/del', market.delete),
    path('api/market/get', market.get),
    path('api/market/getList', market.getList),

    # 权限
    path('api/permission/add', permission.add),
    path('api/permission/del', permission.delete),
    path('api/permission/getList', permission.getList),

    # 角色
    path('api/role/add', role.add),
    path('api/role/set', role.set),
    path('api/role/del', role.delete),
    path('api/role/get', role.get),
    path('api/role/getList', role.getList),

    # 店铺
    path('api/shop/add', shop.add),
    path('api/shop/set', shop.set),
    path('api/shop/del', shop.delete),
    path('api/shop/get', shop.get),
    path('api/shop/getList', shop.getList),

    # 用户-店铺
    path('api/userShop/add', user_shop.add),
    path('api/userShop/del', user_shop.delete),
    path('api/userShop/getList', user_shop.getList),

    # 用户
    path('api/user/add', user.add),
    path('api/user/set', user.set),
    path('api/user/del', user.delete),
    path('api/user/get', user.get),
    path('api/user/getInfo', user.getInfo),
    path('api/user/getByPhone', user.getByPhone),
    path('api/user/getList', user.getList),

    # 订单
    path('api/order/add', order.add),
    path('api/order/set', order.set),
    path('api/order/del', order.delete),
    path('api/order/get', order.get),
    path('api/order/getList', order.getList),

    path('', TemplateView.as_view(template_name='index.html'))
]
