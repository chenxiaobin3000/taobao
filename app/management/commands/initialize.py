from django.core.management.base import BaseCommand
from app.models.system.market import Market
from app.models.system.company import Company
from app.models.system.company_market import CompanyMarket
from app.models.system.role import Role
from app.models.system.permission import Permission
from app.models.system.shop import Shop
from app.models.system.user_shop import UserShop
from app.models.account import Account
from app.models.system.user import User

# 初始化测试数据库
class Command(BaseCommand):
    def handle(self, *args, **options):
        Market.objects.add('淘宝')
        Market.objects.add('抖音')
        Company.objects.add('创想酷玩', 1)
        CompanyMarket.objects.add(1, 1)
        CompanyMarket.objects.add(1, 2)

        Role.objects.add(1, '高管')
        Role.objects.add(1, '运营')
        for i in range(1, 3):
            Permission.objects.add(i, 1000)
            Permission.objects.add(i, 1001)
            Permission.objects.add(i, 2000)
            Permission.objects.add(i, 2001)
            Permission.objects.add(i, 2002)
            Permission.objects.add(i, 2003)
            Permission.objects.add(i, 2004)
            Permission.objects.add(i, 2005)
            Permission.objects.add(i, 2006)
            Permission.objects.add(i, 3000)
            Permission.objects.add(i, 3001)
            Permission.objects.add(i, 3002)
            Permission.objects.add(i, 3003)
            Permission.objects.add(i, 3004)
            Permission.objects.add(i, 3005)
            Permission.objects.add(i, 3006)
            Permission.objects.add(i, 3007)
            Permission.objects.add(i, 3008)
            Permission.objects.add(i, 3009)
            Permission.objects.add(i, 3010)
            Permission.objects.add(i, 4000)
            Permission.objects.add(i, 4001)
            Permission.objects.add(i, 4002)
            Permission.objects.add(i, 4003)
            Permission.objects.add(i, 5000)
            Permission.objects.add(i, 5001)
            Permission.objects.add(i, 5002)
            Permission.objects.add(i, 5003)
            Permission.objects.add(i, 5004)
            Permission.objects.add(i, 5005)
            Permission.objects.add(i, 5006)
            Permission.objects.add(i, 5007)

        Shop.objects.add(1, 1, '德国KSTE')
        Shop.objects.add(1, 1, '挪威VER')
        Shop.objects.add(1, 1, '日本SKLA')
        Shop.objects.add(1, 1, '酷娃KUWA')
        UserShop.objects.add(1, 1)
        UserShop.objects.add(1, 2)
        UserShop.objects.add(1, 3)
        UserShop.objects.add(1, 4)

        Account.objects.add('admin', '21218cca77804d2ba1922c33e0151105', 1)
        User.objects.add('小月', '01234567890', 1, 1)
        print("init success")
