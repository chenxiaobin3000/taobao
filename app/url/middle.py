from django.urls import path
from app.views.middle import fake

url_middle = [
    # 刷单
    path('api/fake/add', fake.add),
    path('api/fake/del', fake.delete),
    path('api/fake/get', fake.get),
    path('api/fake/getList', fake.getList),
]
