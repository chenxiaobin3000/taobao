from django.urls import path
from app.views import account
from app.views.system import company, good, good_alias, good_follow, market, permission, receipt_owner, role, shop, user, user_shop

url_system = [
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
    path('api/company/getList', company.getList),

    # 商品
    path('api/good/addList', good.addList),
    path('api/good/flush', good.flush),
    path('api/good/set', good.set),
    path('api/good/del', good.delete),
    path('api/good/getList', good.getList),
    path('api/good/getInitZip', good.getInitZip),

    # 商品关注
    path('api/good_follow/add', good_follow.add),
    path('api/good_follow/set', good_follow.set),
    path('api/good_follow/del', good_follow.delete),
    path('api/good_follow/getList', good_follow.getList),

    # 商品别名
    path('api/good_alias/add', good_alias.add),
    path('api/good_alias/getById', good_alias.getById),
    path('api/good_alias/getByName', good_alias.getByName),
    path('api/good_alias/del', good_alias.delete),
    path('api/good_alias/delById', good_alias.deleteById),
    path('api/good_alias/getList', good_alias.getList),

    # 平台
    path('api/market/add', market.add),
    path('api/market/set', market.set),
    path('api/market/del', market.delete),
    path('api/market/get', market.get),
    path('api/market/getList', market.getList),

    # 发票主体
    path('api/receipt_owner/add', receipt_owner.add),
    path('api/receipt_owner/del', receipt_owner.delete),
    path('api/receipt_owner/getList', receipt_owner.getList),

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
    path('api/shop/getList', shop.getList),
    path('api/shop/getOwnList', shop.getOwnList),

    # 用户-店铺
    path('api/userShop/add', user_shop.add),
    path('api/userShop/del', user_shop.delete),
    path('api/userShop/getList', user_shop.getList),
    path('api/userShop/getListByShop', user_shop.getListByShop),

    # 用户
    path('api/user/add', user.add),
    path('api/user/set', user.set),
    path('api/user/del', user.delete),
    path('api/user/get', user.get),
    path('api/user/getInfo', user.getInfo),
    path('api/user/getByPhone', user.getByPhone),
    path('api/user/getList', user.getList),
]
