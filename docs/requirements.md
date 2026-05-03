# 需求说明文档

本文档根据当前源码结构、前端路由、权限配置、后端 URL 与模型分层整理而成，用于描述系统已经实现或由源码明确体现的功能需求。文档不包含未在源码中体现的规划能力。

## 1. 项目背景

本系统是一个电商运营与财务数据管理后台，面向多公司、多店铺场景，支持淘宝等平台相关业务数据的导入、归档、汇总和报表分析。

系统通过前端管理台完成数据录入、导入、查询、汇总刷新、报表查看和权限配置；后端提供统一的 `api/` 接口，使用 SQLite 保存业务数据。

## 2. 使用对象

### 2.1 管理员/高管

- 管理公司、店铺、商品、用户、角色和权限。
- 查看全部或授权范围内的报表。
- 重置用户密码。
- 维护系统基础数据。

### 2.2 运营人员

- 导入订单、推广、扣费、退款等原始业务数据。
- 执行数据合并、汇总刷新和异常数据处理。
- 查看订单、刷单、推广、商品、成本等报表。

### 2.3 普通业务用户

- 在被授权店铺范围内查看和维护相关业务数据。
- 修改自己的登录密码。

## 3. 总体功能范围

系统功能按前端权限树和后端接口划分为六大模块：

| 模块 | 权限码 | 功能说明 |
| --- | --- | --- |
| 系统管理 | `1000` | 修改密码等系统级功能 |
| 公司数据 | `2000` | 公司、店铺、商品、用户、角色、密码管理 |
| 原始数据 | `3000` | 原始订单、刷单、推广、扣费、聚合、退款、小额打款等数据管理 |
| 存档数据 | `4000` | 原始数据合并后的业务归档数据管理 |
| 统计报表 | `5000` | 业绩大屏、年报、日报、商品、推广、成本、订单、遗漏报表 |
| 辅助工具 | `6000` | 杂项、订单汇总、刷单汇总、扣款汇总、预备商品等辅助处理 |

## 4. 权限需求

### 4.1 登录权限

- 用户必须登录后才能访问业务页面。
- 未登录用户只能访问登录页和错误页。
- 登录后系统应根据用户权限动态生成可访问菜单。
- 前端权限码来自 `POST /api/user/getInfo` 返回的 `perms`。

### 4.2 菜单权限

菜单权限由 `client/src/utils/role-data.js` 与 `client/src/router/modules/` 定义。

| 权限码 | 菜单/功能 |
| --- | --- |
| `1001` | 修改密码 |
| `2001` | 公司信息 |
| `2002` | 店铺管理 |
| `2003` | 商品管理 |
| `2004` | 用户管理 |
| `2005` | 角色管理 |
| `2006` | 重置密码 |
| `3001` | 原始订单管理 |
| `3002` | 原始刷单管理 |
| `3003` | 原始推广管理 |
| `3004` | 原始推广明细 |
| `3005` | 原始扣费管理 |
| `3006` | 原始扣费过滤 |
| `3007` | 原始聚合管理 |
| `3008` | 原始聚合过滤 |
| `3009` | 原始退货管理 |
| `3010` | 原始退货过滤 |
| `3011` | 原始小额打款 |
| `4001` | 存档订单管理 |
| `4002` | 存档刷单管理 |
| `4003` | 存档推广管理 |
| `4004` | 存档推广明细 |
| `4005` | 存档扣费管理 |
| `4007` | 存档聚合管理 |
| `4009` | 存档退货管理 |
| `4010` | 存档小额打款 |
| `5001` | 业绩大屏 |
| `5002` | 年报汇总 |
| `5003` | 日报汇总 |
| `5004` | 商品汇总 |
| `5005` | 推广汇总 |
| `5006` | 成本汇总 |
| `5007` | 订单汇总 |
| `5008` | 遗漏汇总 |
| `6001` | 杂项管理 |
| `6002` | 订单汇总管理 |
| `6003` | 刷单汇总管理 |
| `6004` | 扣款汇总管理 |
| `6005` | 预备商品 |

## 5. 账号与用户需求

### 5.1 登录

- 用户输入账号和密码。
- 前端使用 MD5 对密码加密后提交。
- 后端校验账号密码。
- 登录成功后返回用户 ID，并由前端保存登录状态。

接口：

```text
POST /api/account/login
```

### 5.2 退出

- 用户可主动退出登录。
- 前端清除本地登录状态、用户 ID、权限和缓存路由。

接口：

```text
POST /api/account/logout
```

### 5.3 修改密码

- 已登录用户可修改自己的密码。
- 修改时需要提交原密码与新密码。
- 后端校验原密码正确后更新账号密码。

接口：

```text
POST /api/account/setPassword
```

### 5.4 重置密码

- 有权限的用户可重置其他用户密码。
- 默认密码常量位于 `app/models/const/default_password.py`。
- 当前默认密码注释为 `888888`，代码中保存的是 MD5 值。

接口：

```text
POST /api/account/resetPassword
```

## 6. 公司数据需求

### 6.1 公司管理

- 支持新增公司。
- 支持修改公司信息。
- 支持删除公司。
- 支持分页或条件查询公司列表。

接口：

```text
POST /api/company/add
POST /api/company/set
POST /api/company/del
POST /api/company/getList
```

### 6.2 店铺管理

- 支持新增、修改、删除和查询店铺。
- 支持查询当前用户可访问的店铺列表。
- 店铺与公司、平台、用户存在关联关系。

接口：

```text
POST /api/shop/add
POST /api/shop/set
POST /api/shop/del
POST /api/shop/getList
POST /api/shop/getOwnList
```

### 6.3 商品管理

- 支持批量新增商品。
- 支持刷新商品相关数据。
- 支持修改、删除和查询商品。
- 支持维护商品别名。
- 商品包含来源平台、进货平台、商品状态、商品类型等字段。

接口：

```text
POST /api/good/addList
POST /api/good/flush
POST /api/good/set
POST /api/good/del
POST /api/good/getList
POST /api/good_alias/add
POST /api/good_alias/getById
POST /api/good_alias/getByName
POST /api/good_alias/del
POST /api/good_alias/delById
POST /api/good_alias/getList
```

### 6.4 平台管理

- 支持新增、修改、删除、查询平台。
- 初始化脚本中包含淘宝、抖音等平台数据。

接口：

```text
POST /api/market/add
POST /api/market/set
POST /api/market/del
POST /api/market/get
POST /api/market/getList
```

### 6.5 用户、角色与权限

- 支持新增、修改、删除和查询用户。
- 支持按手机号查询用户。
- 支持查询用户详情、公司、平台、店铺与权限信息。
- 支持新增、修改、删除和查询角色。
- 支持为角色维护权限码。
- 支持维护用户与店铺的绑定关系。

接口：

```text
POST /api/user/add
POST /api/user/set
POST /api/user/del
POST /api/user/get
POST /api/user/getInfo
POST /api/user/getByPhone
POST /api/user/getList
POST /api/role/add
POST /api/role/set
POST /api/role/del
POST /api/role/get
POST /api/role/getList
POST /api/permission/add
POST /api/permission/del
POST /api/permission/getList
POST /api/userShop/add
POST /api/userShop/del
POST /api/userShop/getList
POST /api/userShop/getListByShop
```

## 7. 原始数据需求

原始数据模块用于保存平台导出或人工整理后的明细数据。部分页面支持 Excel 上传并按批次提交。

前端导入相关常量：

- 每批导入数量：`ImportCount = 500`
- 导入间隔：`ImportSpan = 2000` 毫秒

### 7.1 原始订单

- 支持批量导入订单。
- 支持查询订单列表。
- 支持删除单条订单。
- 支持清空订单数据。
- 订单状态包括交易成功、交易关闭、已发货、待发货、待付款、未创建支付宝交易、异常。

接口：

```text
POST /api/user_order/addList
POST /api/user_order/getList
POST /api/user_order/del
POST /api/user_order/delAll
```

### 7.2 原始刷单

- 支持查询刷单列表。
- 支持删除单条刷单记录。
- 支持清空刷单数据。

接口：

```text
POST /api/user_fake/getList
POST /api/user_fake/del
POST /api/user_fake/delAll
```

### 7.3 原始推广与推广明细

- 支持批量导入推广数据。
- 支持批量导入推广明细。
- 支持查询、删除、清空推广与推广明细。
- 推广类型包括直通车、全站、人群、预支付扣款、异常。

接口：

```text
POST /api/user_promotion/addList
POST /api/user_promotion/getList
POST /api/user_promotion/del
POST /api/user_promotion/delAll
POST /api/user_promotion_detail/addList
POST /api/user_promotion_detail/getList
POST /api/user_promotion_detail/del
POST /api/user_promotion_detail/delAll
```

### 7.4 原始扣费与扣费过滤

- 支持批量导入扣费数据。
- 支持查询、删除、清空扣费数据。
- 支持查询、删除、清空被过滤的扣费数据。
- 扣费类型覆盖服务费、营销礼金、跨境服务费、赔付红包、保证金、充值、转账、退款等。

接口：

```text
POST /api/user_deduction/addList
POST /api/user_deduction/getList
POST /api/user_deduction/del
POST /api/user_deduction/delAll
POST /api/user_deduction_discard/getList
POST /api/user_deduction_discard/del
POST /api/user_deduction_discard/delAll
```

### 7.5 原始聚合与聚合过滤

- 支持批量导入聚合数据。
- 支持查询、删除、清空聚合数据。
- 支持查询、删除、清空被过滤的聚合数据。

接口：

```text
POST /api/user_polymerize/addList
POST /api/user_polymerize/getList
POST /api/user_polymerize/del
POST /api/user_polymerize/delAll
POST /api/user_polymerize_discard/getList
POST /api/user_polymerize_discard/del
POST /api/user_polymerize_discard/delAll
```

### 7.6 原始采购

- 支持批量导入采购数据。
- 支持查询、删除、清空采购数据。

接口：

```text
POST /api/user_purchase/addList
POST /api/user_purchase/getList
POST /api/user_purchase/del
POST /api/user_purchase/delAll
```

### 7.7 原始退货与退货过滤

- 支持批量导入退货/退款数据。
- 支持查询、删除、清空退货数据。
- 支持查询、删除、清空被过滤的退货赠品/异常数据。
- 退款状态包括退款成功、退款关闭、申请退款、同意退款、买家退货、换货、重新邮寄、拒绝退款、异常。
- 退款类型包括仅退款、退货退款、换货、补寄、退款、退运费、维修、邮费退差、异常。

接口：

```text
POST /api/user_refund/addList
POST /api/user_refund/getList
POST /api/user_refund/del
POST /api/user_refund/delAll
POST /api/user_refund_gift/getList
POST /api/user_refund_gift/del
POST /api/user_refund_gift/delAll
```

### 7.8 原始小额打款

- 支持批量导入小额打款数据。
- 支持查询、删除、清空小额打款数据。

接口：

```text
POST /api/user_transfer/addList
POST /api/user_transfer/getList
POST /api/user_transfer/del
POST /api/user_transfer/delAll
```

## 8. 存档数据需求

存档数据模块用于把原始数据合并为可长期查询和参与报表统计的核心业务数据。

### 8.1 合并要求

- 每类存档数据均提供 `merge` 操作。
- 合并过程应根据店铺、用户、商品、订单号、业务类型等信息整理原始记录。
- 合并结果保存到对应 `trunk` 模型表。

### 8.2 查询与删除

- 每类存档数据均支持列表查询。
- 每类存档数据均支持删除单条记录。

接口：

```text
POST /api/order/merge
POST /api/order/getList
POST /api/order/del
POST /api/fake/merge
POST /api/fake/getList
POST /api/fake/del
POST /api/promotion/merge
POST /api/promotion/getList
POST /api/promotion/del
POST /api/promotion_detail/merge
POST /api/promotion_detail/getList
POST /api/promotion_detail/del
POST /api/deduction/merge
POST /api/deduction/getList
POST /api/deduction/del
POST /api/polymerize/merge
POST /api/polymerize/getList
POST /api/polymerize/del
POST /api/purchase/merge
POST /api/purchase/getList
POST /api/purchase/del
POST /api/refund/merge
POST /api/refund/getList
POST /api/refund/del
POST /api/transfer/merge
POST /api/transfer/getList
POST /api/transfer/del
```

## 9. 辅助工具需求

### 9.1 订单汇总

- 支持刷新订单汇总数据。
- 支持查询订单汇总列表。
- 汇总逻辑基于订单、刷单、退款、小额打款、扣款等数据生成订单级或日期级汇总。

接口：

```text
POST /api/order_summary/flush
POST /api/order_summary/getList
```

### 9.2 刷单汇总

- 支持刷新刷单汇总。
- 支持修改刷单汇总记录。
- 支持设置刷单汇总完成状态。
- 支持批处理刷单汇总。
- 支持查询刷单汇总列表。

接口：

```text
POST /api/fake_summary/flush
POST /api/fake_summary/set
POST /api/fake_summary/setComplete
POST /api/fake_summary/batch
POST /api/fake_summary/getList
```

### 9.3 扣款汇总

- 支持刷新扣款汇总。
- 支持查询扣款汇总列表。
- 汇总逻辑会生成或使用遗漏记录，用于报表中的遗漏分析。

接口：

```text
POST /api/deduction_summary/flush
POST /api/deduction_summary/getList
```

### 9.4 预备商品

- 支持新增预备商品。
- 支持刷新预备商品。
- 支持删除预备商品。
- 支持查询预备商品列表。

接口：

```text
POST /api/good_prepare/add
POST /api/good_prepare/flush
POST /api/good_prepare/del
POST /api/good_prepare/getList
```

### 9.5 杂项管理

- 支持新增杂项。
- 支持修改杂项。
- 支持删除杂项。
- 支持查询杂项列表。

接口：

```text
POST /api/misc/add
POST /api/misc/set
POST /api/misc/del
POST /api/misc/getList
```

### 9.6 发票相关数据

源码提供进项票、发票项和发票维护接口，但当前前端菜单未直接暴露这些页面。

接口：

```text
POST /api/receipt_from/add
POST /api/receipt_from/del
POST /api/receipt_from/getList
POST /api/receipt_item/add
POST /api/receipt_item/del
POST /api/receipt_item/getList
POST /api/receipt_to/add
POST /api/receipt_to/del
POST /api/receipt_to/getList
```

## 10. 报表需求

### 10.1 业绩大屏

- 展示关键经营指标。
- 数据来源包括订单、刷单、推广等统计模型。

接口：

```text
POST /api/board_report/getList
```

### 10.2 年报汇总

- 按年度/月度汇总订单、刷单、推广等经营数据。
- 用于查看全年趋势。

接口：

```text
POST /api/year_report/getList
```

### 10.3 日报汇总

- 按日期展示日维度经营数据。
- 支持根据店铺和时间范围查询。

接口：

```text
POST /api/day_report/getList
```

### 10.4 商品汇总

- 展示商品维度的经营数据。
- 支持商品关注状态维护。
- 支持关注、取消关注、查询关注列表。

接口：

```text
POST /api/good_report/getList
POST /api/good_follow/add
POST /api/good_follow/set
POST /api/good_follow/del
POST /api/good_follow/getList
```

### 10.5 推广汇总

- 展示推广相关统计结果。
- 源码路由注释中存在“商品雷达”描述，前端菜单显示为“推广汇总”。

接口：

```text
POST /api/promotion_report/getList
```

### 10.6 成本汇总

- 展示成本相关统计结果。

接口：

```text
POST /api/cost_report/getList
```

### 10.7 订单汇总

- 展示订单相关统计列表。
- 可结合订单状态、扣款类型等维度筛选。

接口：

```text
POST /api/order_report/getList
```

### 10.8 遗漏汇总

- 展示扣款、订单或汇总过程产生的遗漏数据。

接口：

```text
POST /api/omission_report/getList
```

### 10.9 刷单报表

后端提供刷单报表接口，当前权限树没有单独暴露“刷单报表”菜单。

接口：

```text
POST /api/fake_report/getList
```

## 11. 数据流需求

系统核心数据流如下：

1. 用户维护公司、平台、店铺、商品、用户、角色和权限。
2. 运营人员导入原始订单、扣费、推广、退款、采购、聚合、小额打款等数据。
3. 用户执行存档数据合并，将原始数据转换为核心业务数据。
4. 用户执行辅助汇总刷新，生成订单汇总、扣款汇总、刷单汇总、日汇总等中间结果。
5. 报表模块基于存档数据、汇总数据和原生 SQL 查询生成统计结果。
6. 前端根据用户权限展示对应菜单和页面。

## 12. 数据字典概要

### 12.1 订单状态

- 交易成功
- 交易关闭
- 卖家已发货，等待买家确认
- 买家已付款，等待卖家发货
- 等待买家付款
- 未创建支付宝交易
- 异常

### 12.2 商品状态

- 在售
- 下架
- 删除
- 异常

### 12.3 商品类型

- 商品
- 赠品
- 补差价
- 异常

### 12.4 商品来源

- 淘宝
- 天猫
- 异常

### 12.5 商品进货平台

- 1688
- 淘宝
- 拼多多
- 抖音
- 异常

### 12.6 财务类型

- 保证金
- 分账
- 在线支付
- 转账
- 退款
- 其他
- 扣款
- 交易收款
- 提现
- 公共缴费
- 异常

### 12.7 退款类型

- 仅退款
- 退货退款
- 换货
- 补寄
- 退款
- 退运费
- 维修
- 邮费退差
- 异常

## 13. 接口通用约定

### 13.1 请求方式

- 后端视图多数使用 `@require_POST`，业务接口应使用 `POST`。
- 前端统一通过 `client/src/utils/request.js` 的 Axios 实例请求。
- 开发环境前端请求 `/api`，由 Vue devServer 代理到 `http://localhost:8000/api`。

### 13.2 响应格式

接口通常返回以下结构：

```json
{
  "code": 0,
  "msg": "success",
  "data": {}
}
```

### 13.3 错误处理

- `code === 0` 表示成功。
- `code !== 0` 表示业务失败，前端会展示 `msg`。
- `code === -3` 时前端会提示重新登录。
- HTTP `400` 会展示后端返回的错误信息。
- 其他网络异常会提示网络异常。

## 14. 非功能需求

### 14.1 运行环境

后端：

- Python 3.x
- Django 5.2.8
- django-cors-headers
- SQLite

前端：

- Node.js `>= 8.9`
- npm `>= 3.0.0`
- Vue CLI 4

### 14.2 性能与数据量

- 当前数据库为 SQLite，适合本地开发、单机部署和中小规模数据。
- 大量 Excel 导入通过批次和间隔控制，降低单次请求压力。
- 报表部分使用原生 SQL 查询，后续数据量增长时需要关注索引和查询耗时。

### 14.3 安全

- 登录密码在前端使用 MD5 后提交。
- 生产环境需要关闭 `DEBUG`。
- 生产环境需要配置 `ALLOWED_HOSTS`。
- 生产环境应将 `SECRET_KEY` 从源码迁移到环境变量或安全配置。
- 角色权限仅控制前端菜单和接口访问范围，后续如需更强安全性，建议在后端补充统一鉴权中间件或装饰器。

### 14.4 可维护性

- 后端按 `system`、`original`、`trunk`、`middle`、`report` 分层组织。
- 前端按 `api`、`views`、`router/modules` 分层组织。
- 业务常量在前后端均有定义，后续变更时需要同步维护。
- 当前仓库没有后端依赖锁定文件，建议补充 `requirements.txt`。

## 15. 初始化与部署需求

### 15.1 初始化

系统提供初始化命令：

```bash
python manage.py initialize
```

初始化内容包括平台、公司、角色、权限、店铺、用户和账号等基础数据。执行前应确认当前数据库是否允许写入这些默认数据。

### 15.2 本地运行

后端：

```bash
python manage.py runserver
```

前端：

```bash
cd client
npm install
npm run dev
```

### 15.3 构建部署

前端构建：

```bash
cd client
npm run build
```

部署脚本：

```bat
client\deploy.bat
```

该脚本会把前端构建产物复制到 Django 的 `static/` 和 `app/templates/`。

## 16. 已知约束与风险

- 当前部分历史源码注释或旧文档存在编码乱码，需求含义以可正常读取的路由、权限树、页面和接口为准。
- 账号登录接口当前主要返回用户 ID，前端仍保存 `token` 字段；后端源码中 token/session 校验逻辑并不完整。
- SQLite 在高并发或大数据量场景下可能成为瓶颈。
- 部分后端接口已存在，但前端菜单未暴露，如发票相关接口和刷单报表接口。
- 前后端存在重复业务常量，后续应考虑抽取统一配置或增加同步校验。
