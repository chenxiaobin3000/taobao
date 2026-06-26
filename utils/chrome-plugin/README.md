# Taobao Good Image Saver

Chrome 插件用于在已登录的淘宝/天猫商品页保存商品缩略图。

## 店铺列表

店铺列表写死在 `popup.js` 的 `SHOP_LIST` 常量里：

```js
const SHOP_LIST = [
  { id: 1, name: '德国KSTE' },
  { id: 2, name: '挪威VER' },
  { id: 3, name: '日本SKLA' },
  { id: 5, name: '法国FALS' },
  { id: 4, name: '酷娃KUWA' }
]
```

后续店铺变化时，直接修改这个数组。

## 安装

1. 打开 Chrome 扩展程序页面：`chrome://extensions/`
2. 打开“开发者模式”
3. 点击“加载已解压的扩展程序”
4. 选择本目录：`utils/chrome-plugin`

## 使用

1. 建议把 Chrome 默认下载目录设置为项目的 `static` 目录：`C:\dev\taobao\static`
2. 打开淘宝或天猫商品页，URL 里需要有 `id=淘宝商品ID`
3. 点击插件图标，选择店铺
4. 点击“保存缩略图”

文件会下载到：

```text
static/good_images/<店铺ID>/<淘宝商品ID>.jpg
```

项目商品列表会按商品的外部编码查找图片，所以文件名使用淘宝商品 ID，不使用内部商品编码。
