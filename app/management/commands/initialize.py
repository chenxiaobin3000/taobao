from django.core.management.base import BaseCommand
from app.models.system.market import Market
from app.models.account import Account
from app.models.system.user import User

# 初始化测试数据库
class Command(BaseCommand):
    def handle(self, *args, **options):
        Market.objects.add('taobao')
        Account.objects.add('admin', '21218cca77804d2ba1922c33e0151105', 1)
        User.objects.add('test', '01234567890', 1, 1)
        print("init success")
