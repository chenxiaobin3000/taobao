# Taobao Admin

一个面向电商运营/财务数据处理的后台管理系统。项目采用 Django 提供 API 与数据处理能力，Vue 2 + Element UI 提供管理端界面，主要围绕淘宝等平台店铺的原始数据导入、归档合并、辅助汇总和统计报表展开。

## 项目概览

- 后端：Django 项目，入口为 `manage.py`，配置目录为 `server/`，业务应用为 `app/`。
- 前端：Vue CLI 项目，位于 `client/`，开发环境通过代理访问后端接口。
- 数据库：默认使用根目录下的 SQLite 数据库 `cxkw.db`。
- 部署形态：前端构建产物复制到 Django 的 `static/` 和 `app/templates/`，由 Django 返回 `index.html` 并提供 API。

## 技术栈

### 后端

- Python 3.x
- Django 5.2.8
- django-cors-headers
- SQLite

### 前端

- Vue 2.6
- Vue Router 3
- Vuex 3
- Element UI 2
- Axios
- ECharts
- xlsx / file-saver
- Vue CLI 4

## 目录结构

```text
taobao/
├── app/                         # Django 业务应用
│   ├── management/commands/      # 自定义管理命令，如 initialize
│   ├── models/                   # 数据模型与原生 SQL 查询对象
│   │   ├── const/                # 业务常量
│   │   ├── middle/               # 汇总/辅助表模型
│   │   ├── original/             # 原始导入数据模型
│   │   ├── report/               # 报表查询模型
│   │   ├── system/               # 公司、店铺、用户、角色等系统模型
│   │   └── trunk/                # 归档后的核心业务数据模型
│   ├── templates/                # Django 模板，生产环境放置前端 index.html
│   ├── url/                      # 按业务模块拆分的 URL 配置
│   └── views/                    # API 视图
├── client/                       # Vue 前端项目
│   ├── public/
│   └── src/
│       ├── api/                  # 前端 API 封装
│       ├── components/           # 通用组件
│       ├── layout/               # 后台布局
│       ├── router/               # 路由与权限菜单
│       ├── store/                # Vuex 状态管理
│       └── views/                # 页面
├── server/                       # Django 项目配置
├── static/                       # Django 静态资源目录
├── backup/                       # 数据库备份目录
├── cxkw.db                       # SQLite 数据库
├── manage.py                     # Django 管理入口
└── *.bat                         # Windows 常用脚本
```

## 核心业务模块

### 系统与权限

对应目录：

- 后端：`app/views/system/`、`app/models/system/`
- 前端：`client/src/views/company/`、`client/src/views/system/`

主要能力：

- 账号登录、退出、修改密码、重置密码
- 公司管理
- 店铺管理
- 商品与商品别名管理
- 用户、角色、权限管理
- 用户与店铺关系维护

### 原始数据

对应目录：

- 后端：`app/views/original/`、`app/models/original/`
- 前端：`client/src/views/original/`

主要数据类型：

- 订单
- 刷单
- 推广
- 推广明细
- 扣费
- 聚合
- 采购
- 退货/退款
- 小额打款

这些模块通常负责批量导入、查询、删除和清空原始业务数据。

### 归档数据

对应目录：

- 后端：`app/views/trunk/`、`app/models/trunk/`
- 前端：`client/src/views/trunk/`

主要能力：

- 将原始数据合并为归档数据
- 查询归档后的订单、刷单、推广、扣费、聚合、退货、小额打款等记录
- 删除归档记录

### 辅助工具与汇总

对应目录：

- 后端：`app/views/middle/`、`app/models/middle/`
- 前端：`client/src/views/middle/`

主要能力：

- 订单汇总刷新
- 扣款汇总刷新
- 刷单汇总刷新与批处理
- 预备商品维护
- 杂项管理
- 发票相关数据维护

### 统计报表

对应目录：

- 后端：`app/views/report/`、`app/models/report/`
- 前端：`client/src/views/report/`

主要报表：

- 业绩大屏
- 年报汇总
- 日报汇总
- 商品汇总
- 推广汇总
- 成本汇总
- 订单汇总
- 遗漏汇总

部分报表查询使用 `app/models/report/native_*.py` 中的原生 SQL，主要面向汇总表进行统计。

## 本地开发

### 1. 后端环境

建议使用虚拟环境：

```bash
python -m venv .venv
.venv\Scripts\activate
```

安装依赖：

```bash
pip install django django-cors-headers
```

项目当前没有提交 `requirements.txt`，如果后续新增依赖，建议补充依赖清单。

### 2. 数据库迁移

```bash
python manage.py makemigrations app
python manage.py migrate
```

Windows 下也可以使用已有脚本：

```bat
makemigrations.bat
migrate.bat
```

### 3. 初始化数据

项目提供了自定义命令：

```bash
python manage.py initialize
```

或使用：

```bat
init.bat
```

注意：初始化命令会写入默认平台、公司、角色、权限、店铺、用户和账号数据。当前部分历史文件存在编码显示异常，执行前建议确认初始化数据符合当前环境。

### 4. 启动后端

```bash
python manage.py runserver
```

默认访问：

```text
http://localhost:8000/
```

也可以使用根目录脚本：

```bat
server.bat
```

`server.bat` 会先备份数据库、清理缓存、执行迁移，再启动 Django 服务。

### 5. 启动前端

```bash
cd client
npm install
npm run dev
```

默认前端开发服务：

```text
http://localhost:9527/
```

开发环境下，`client/vue.config.js` 会把 `/api` 代理到：

```text
http://localhost:8000/api
```

## 构建与部署

前端构建：

```bash
cd client
npm run build
```

构建后可以执行：

```bat
client\deploy.bat
```

该脚本会：

- 清理根目录 `static/` 下旧的前端静态资源
- 将 `client/dist/static/` 复制到根目录 `static/`
- 将 `client/dist/index.html` 复制到 `app/templates/`

Django 根路由 `server/urls.py` 会返回 `app/templates/index.html`，API 仍由 `api/...` 路径提供。

## 常用脚本

| 脚本 | 作用 |
| --- | --- |
| `init.bat` | 执行 `python manage.py initialize` |
| `makemigrations.bat` | 为 `app` 生成迁移文件 |
| `migrate.bat` | 执行数据库迁移 |
| `server.bat` | 备份数据库、清理缓存、迁移并启动后端 |
| `backup.bat` | 将 `cxkw.db` 复制到 `backup/` 并追加时间戳 |
| `clean.bat` | 清理 Python 缓存和迁移缓存 |
| `client/server.bat` | 启动前端开发服务 |
| `client/deploy.bat` | 部署前端构建产物到 Django 静态目录 |

## 接口约定

后端接口集中在 `app/url/` 中，统一使用 `api/` 前缀。前端 API 封装位于 `client/src/api/`。

常见接口风格：

```text
POST /api/account/login
POST /api/user/getInfo
POST /api/order/getList
POST /api/order/merge
POST /api/order_summary/flush
POST /api/year_report/getList
```

大多数接口返回类似结构：

```json
{
  "code": 0,
  "msg": "success",
  "data": {}
}
```

前端 `client/src/utils/request.js` 会拦截响应，当 `code !== 0` 时显示错误消息。

## 登录与权限

- 登录接口：`POST /api/account/login`
- 前端登录时会对明文密码做 MD5 后提交。
- 登录后前端保存 `userId` 和 `token` 到本地缓存。
- 权限菜单由 `client/src/router/modules/` 中的 `roles` 权限码控制。
- 用户权限从 `POST /api/user/getInfo` 获取。

默认密码常量位于：

```text
app/models/const/default_password.py
```

当前默认密码注释为 `888888`，代码中存储的是对应 MD5 值。

## 数据流说明

项目的数据处理大致分为四层：

1. 原始数据：导入平台或人工整理后的业务明细，存入 `t_user_*` 表。
2. 归档数据：通过 `merge` 接口把原始数据整理到核心业务表，如订单、退款、推广、扣费等。
3. 汇总数据：通过 `flush` 或批处理接口生成订单汇总、扣款汇总、日汇总等中间表。
4. 报表数据：报表模块基于归档表和汇总表进行统计查询，并返回给前端图表或列表页面。

## 注意事项

- 当前后端配置为 `DEBUG = True`，生产环境应关闭。
- 当前 `ALLOWED_HOSTS = []`，生产环境需要配置允许访问的域名或 IP。
- `SECRET_KEY` 已写在源码中，生产环境应改为环境变量或安全配置。
- SQLite 适合轻量部署和本地开发；数据量或并发增长后建议评估 MySQL/PostgreSQL。
- 前端依赖版本较老，建议使用与项目兼容的 Node.js 版本，避免直接用过新的 Node/npm 造成构建问题。
- 仓库中存在历史编码异常的中文注释和文案，建议后续统一保存为 UTF-8。
- `clean.bat` 会删除迁移相关缓存文件，使用前请确认不会影响当前开发中的迁移记录。

## 后续维护建议

- 增加 `requirements.txt` 或 `pyproject.toml` 固化后端依赖。
- 增加 `.env.example`，把密钥、数据库路径、前端 API 地址等配置外置。
- 为导入、合并、汇总和报表核心流程补充测试。
- 梳理并修复历史乱码，统一项目文件编码。
- 如果继续使用 SQLite，建议保留定期备份机制并验证备份可恢复。
