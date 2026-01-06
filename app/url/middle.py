from django.urls import path
from app.views.middle import fake, miscellaneous

url_middle = [
    # 刷单
    path('api/fake/flush', fake.flush),
    path('api/fake/set', fake.set),
    path('api/fake/getList', fake.getList),

    # 杂项
    path('api/misc/add', miscellaneous.add),
    path('api/misc/set', miscellaneous.set),
    path('api/misc/del', miscellaneous.delete),
    path('api/misc/getList', miscellaneous.getList),
]
