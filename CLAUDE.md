# Admin

## 项目概述
电商/财务管理系统，使用 Django 5.2.8 + SQLite 数据库。

## 技术栈
- **框架**: Django 5.2.8
- **数据库**: SQLite (`cxkw.db`)
- **Python**: 3.10+
- **CORS**: django-cors-headers

## 目录结构
```
taobao/
├── app/                      # 主应用
│   ├── models/               # 模型层
│   │   ├── const/            # 常量定义
│   │   ├── middle/           # 中间表/汇总表
│   │   ├── original/         # 原始业务表
│   │   ├── report/           # 报表模型
│   │   ├── system/           # 系统配置
│   │   └── trunk/            # 核心业务表
│   ├── url/                  # URL 路由
│   ├── views/                # 视图层
│   │   ├── middle/
│   │   ├── original/
│   │   ├── report/
│   │   ├── system/
│   │   └── trunk/
│   └── templates/            # 模板
├── server/                   # Django 配置
├── client/                   # 前端资源
├── static/                   # 静态文件
└── backup/                   # 备份目录
```

## 核心模块

### models/ 结构
- **const/**: 常量定义 (订单状态、商品类型、退款类型等)
- **original/**: 原始业务数据表 (user_order, user_refund, user_promotion 等)
- **trunk/**: 核心业务聚合表 (deduction, order, purchase, refund 等)
- **middle/**: 汇总表 (day_summary, order_summary, deduction_summary 等)
- **report/**: 报表查询类 (order, promotion, fake, cost, day, year)
- **system/**: 系统管理 (user, role, permission, company, shop)

### 报表模块 (`app/models/report/`)
| 文件 | 功能 |
|------|------|
| order.py | 订单统计 (total, totalByStatus, groupByDate, groupByMonth) |
| promotion.py | 推广统计 |
| fake.py | 刷单统计 |
| day.py | 日报相关 |
| cost.py | 成本报表 |
| year.py | 年报 (按月统计全年数据) |

### 视图模块 (`app/views/report/`)
| 文件 | 功能 |
|------|------|
| day_report.py | 日报视图 |
| year_report.py | 年报视图 (按月分组统计) |
| order_report.py | 订单报表视图 |
| promotion_report.py | 推广报表视图 |
| fake_report.py | 刷单报表视图 |
| good_report.py | 商品报表视图 |
| cost_report.py | 成本报表视图 |
| omission_report.py | 遗漏报表视图 |

## 运行命令
```bash
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
python manage.py initialize  # 初始化数据
```

## 常用常量位置
- `app/models/const/order_status.py` - 订单状态
- `app/models/const/refund_status.py` - 退款状态
- `app/models/const/good_status.py` - 商品状态
- `app/models/const/good_type.py` - 商品类型
- `app/models/const/promotion_type.py` - 促销类型
- `app/models/const/company_status.py` - 公司状态
- `app/models/const/deduction_type.py` - 扣款类型
- `app/models/const/omission_order.py` - 减免类型
- `app/models/const/omission_source.py` - 减免来源
- `app/models/const/refund_type.py` - 退款类型

## 数据库表
主要汇总表:
- `t_order_summary` - 订单汇总
- `t_day_summary` - 日报汇总
- `t_promotion_summary` - 推广汇总
- `t_fake_summary` - 刷单汇总
- `t_deduction_summary` - 扣款汇总
- `t_user_order` - 用户订单
- `t_user_refund` - 用户退款
- `t_user_promotion` - 用户推广
- `t_user_purchase` - 用户采购
- `t_user_transfer` - 用户转账
- `t_user_deduction` - 用户扣款

## 注意事项
1. 数据库使用 SQLite，生产环境需考虑性能优化
2. 配置中 `DEBUG = True`, 生产需关闭
3. `ALLOWED_HOSTS = []`, 生产需配置允许的主机
4. SECRET_KEY 需更换为安全值
5. 报表查询使用原始 SQL，注意性能

## 报表查询示例
- 订单年报：`POST /api/year_report/getList`
- 日报：`POST /api/day_report/getList`
- 订单报表：`POST /api/order_report/getList`
- 推广报表：`POST /api/promotion_report/getList`
