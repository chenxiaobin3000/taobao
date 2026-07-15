# Taobao Admin — 项目指南

## 项目概述

电商运营/财务数据处理后台管理系统。后端 Django 提供 API 与数据处理，前端 Vue 2 + Element UI 提供管理界面。

- 项目名：**创想酷玩**
- 作者：cxb <chenxiaobin3000@gmail.com>
- 数据库：SQLite (`cxkw.db`)

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python 3.10+ / Django 5.2.8 / django-cors-headers |
| 前端 | Vue 2.6 / Vue Router 3 / Vuex 3 / Element UI 2.13 / ECharts 4.2 |
| 构建 | Vue CLI 4 (前端) / Django manage.py (后端) |
| OCR | PaddleOCR 3.3 + PaddlePaddle 3.2 (发票识别) |

## 目录结构

```
/
├── app/                      # Django 业务应用
│   ├── management/commands/   # 自定义命令 (initialize)
│   ├── middleware/             # token_auth_middleware (自定义 token 鉴权)
│   ├── models/                 # 数据模型
│   │   ├── const/              # 业务常量 (含默认密码)
│   │   ├── system/             # 公司/店铺/用户/角色/权限表
│   │   ├── original/           # 原始导入数据表 (t_user_*)
│   │   ├── trunk/              # 归档业务数据表
│   │   ├── middle/             # 汇总/辅助表
│   │   └── report/             # 报表查询 (含原生 SQL: native_*.py)
│   ├── templates/              # 生产环境 index.html
│   ├── url/                    # 按模块拆分 (system/original/trunk/middle/report)
│   └── views/                  # 按模块拆分 (system/original/trunk/middle/report)
├── client/                    # Vue 前端 (Vue CLI 4)
│   └── src/
│       ├── api/                # 按模块拆分的 API 封装
│       ├── router/modules/     # 路由+权限菜单 (按角色ID控制)
│       ├── store/              # Vuex 状态
│       ├── views/              # 页面组件
│       └── layout/             # 后台布局
├── server/                    # Django 项目配置 (settings.py / urls.py / wsgi.py)
├── static/                    # 前端构建产物 (css/js/fonts)
└── utils/                     # Chrome 插件 (数据采集辅助)
```

## 快速命令

### 后端
```bash
python manage.py runserver              # 启动 (localhost:8000)
python manage.py makemigrations app      # 生成迁移
python manage.py migrate                 # 执行迁移
python manage.py initialize              # 初始化基础数据
```
或使用 bat 脚本: `server.bat` (备份→迁移→启动)、`init.bat`、`makemigrations.bat`、`migrate.bat`、`backup.bat`、`clean.bat`

### 前端
```bash
cd client && npm install && npm run dev    # 开发 (localhost:9527)
cd client && npm run build                 # 构建
```
构建后执行 `client/deploy.bat` 复制产物到 Django 的 `static/` 和 `app/templates/`

## 核心业务分层

1. **原始数据** (`app/views/original/` + `app/models/original/`) — 批量导入、查询、删除/清空平台原始业务数据 (订单/刷单/推广/推广明细/扣费/聚合/采购/退货/小额打款)
2. **归档数据** (`app/views/trunk/` + `app/models/trunk/`) — merge 接口将原始数据合并到核心业务表，查询/删除归档记录
3. **汇总/辅助** (`app/views/middle/` + `app/models/middle/`) — flush 接口刷新订单汇总/扣款汇总/刷单汇总，上新商品/杂项/发票管理/运营成本
4. **统计报表** (`app/views/report/` + `app/models/report/`) — 业绩大屏/年报/日报/商品/推广/成本/订单/遗漏等报表 (部分使用原生 SQL)

## 代码约定

### 后端
- 视图返回统一格式: `{"code": 0, "msg": "success", "data": {}}` (code ≠ 0 表示错误)
- 自定义中间件鉴权: header 传 `token`，登录/注册接口豁免
- 路由统一 `api/` 前缀，按模块在 `app/url/*.py` 中注册
- 不使用 DRF/Django Admin，均为 `HttpRequest` + `JsonResponse` 原生视图
- URL 配置在 `server/urls.py` 中合并各模块
- 模型文件分散在 `app/models/*/` 子目录，`app/models/model.py` 包含原生查询 SQL
- `app/models/const/default_password.py` 存放默认密码常量 (当前为 888888 的 MD5)

### 前端
- 路由守卫: `client/src/permission.js` 中根据角色ID动态生成可访问路由
- 菜单权限: `client/src/router/modules/*.js` 中 `meta.roles` 数组控制可见性
  - 1000 = 系统功能, 2000 = 公司数据, 3000 = 原始数据, 4000 = 存档数据, 5000 = 统计报表, 6000 = 辅助工具
- API 封装在 `client/src/api/` 按模块拆分
- 登录时密码 MD5 加密后提交
- 请求拦截: `client/src/utils/request.js`，响应 code ≠ 0 时自动提示错误

## 重要注意事项

- **DEBUG = True** 生产环境应关闭；**SECRET_KEY** 在源码中，生产环境应迁移到环境变量
- **ALLOWED_HOSTS** 当前 DEBUG 下为 `['*']`，生产环境需配置
- SQLite 适合轻量部署，数据量增长后建议评估 MySQL/PostgreSQL
- 前端依赖较老，建议使用 Node.js 兼容版本 (>=8.9) 避免构建问题
- 新增接口: 在 `app/views/*` 编写视图 → 注册到 `app/url/*.py` → 前端 `client/src/api/` 添加封装
- 新增报表: 优先查看 `app/models/report/native_*.py` 中现有原生 SQL 模式
- 前端构建产物 (dist/) 通过 deploy.bat 部署到 Django，gitignore 已排除 static/ 和 templates/index.html
- 部分历史文件编码存在异常，建议统一使用 UTF-8
- `.gitignore` 排除了 `cxkw.db`，数据库变更不会纳入版本控制
