// 默认空时间
export const NoneTime = '2000-01-01 00:00:00'

// 默认空订单
export const DefaultOrder = '0000000000000000000'

// 批次导入数量
export const ImportCount = 500

// 导入间隔时间
export const ImportSpan = 2000

// 公司状态
export const CompanyStatus = {
  NORMAL: 1, // 正常
  CLOSE: 2, // 停业
  OTHER: 3, // 异常

  text2num(text) {
    if (text === '正常') {
      return this.NORMAL
    } else if (text === '停业') {
      return this.CLOSE
    } else { // 异常
      return this.OTHER
    }
  },
  num2text(num) {
    switch (num) {
      case this.NORMAL:
        return '正常'
      case this.CLOSE:
        return '停业'
    }
    return '异常'
  }
}

// 扣款状态
export const DeductionType = {
  // 有订单信息
  FU_WU_FEI: 1, // 基础软件服务费
  XIN_XIANG: 2, // 品牌新享淘宝新客营销
  XIN_KE: 3, // 淘宝新客礼金技术服务费
  TI_YAN: 4, // 消费者体验提升计划服务费
  TAO_JIN_BI: 5, // 淘金币软件服务费
  XIAN_YONG_HOU_FU: 6, // 先用后付技术服务费()
  XIAN_YONG_TIAO_ZHANG: 7, // 先用后付技术服务费-
  KUA_JING_JI_CHU: 8, // 淘宝天猫跨境服务基础费
  KUA_JING_ZENG_ZHI: 9, // 淘宝天猫跨境服务增值费
  KUA_JING_DA_JIAN: 10, // 出海增长计划中大件跨境服务增值费
  TAO_TE: 11, // 淘特营销推广服务费
  XIAN_SHI: 12, // 限时红包代商家垫付扣回
  XIN_PIN: 13, // 品牌新享淘宝新品营销
  XIN_XIANG_FU_WU: 14, // 品牌新享-淘宝营销托管
  XIAO_FEI_QUAN: 15, // 消费券代付资金扣回
  GUAN_KONG: 16, // 保证金管控资金使用
  XIAN_SHI_LI_JIN: 17, // 限时礼金软件服务费
  JI_YUN_WU_LIU: 18, // 商家集运物流服务费
  JI_YUN_CAO_ZUO_FEI: 19, // 商家集运中转操作费

  // 无订单信息
  GONG_YI: 100, // 公益宝贝捐赠
  YAN_CHI_FA_HUO: 101, // 卖家延迟发货赔付红包
  XU_JIA_FA_HUO: 102, // 虚假发货赔付红包
  WU_LIU_YI_CHANG: 103, // 淘宝物流轨迹异常红包
  QUE_HUO: 104, // 淘宝缺货赔付红包
  HUA_BEI: 105, // 花呗分期免息营销
  WU_LIU_CHAO_SHI: 106, // 淘宝物流轨迹超时红包
  YAN_CHI_HUAN_HUO: 107, // 延迟换货补偿红包

  // 不处理
  TUI_KUAN: 200, // 退款
  ZHUAN_ZHANG: 201, // 转账
  BAO_ZHENG_JIN: 202, // 淘宝消费者保证金
  DA_KUAN: 203, // 支付宝转账小额打款
  CHONG_ZHI: 204, // 万相台无界版自动充值
  ONLINE: 205, // 在线支付

  OTHER: 1000, // 异常

  text2num(text) {
    if (text.indexOf('基础软件服务费') !== -1) {
      return this.FU_WU_FEI
    } else if (text.indexOf('品牌新享淘宝新客营销') !== -1) {
      return this.XIN_XIANG
    } else if (text.indexOf('淘宝新客礼金技术服务费') !== -1) {
      return this.XIN_KE
    } else if (text.indexOf('消费者体验提升计划服务费') !== -1) {
      return this.TI_YAN
    } else if (text.indexOf('淘金币软件服务费') !== -1) {
      return this.TAO_JIN_BI
    } else if (text.indexOf('先用后付技术服务费(') !== -1) {
      return this.XIAN_YONG_HOU_FU
    } else if (text.indexOf('先用后付技术服务费-') !== -1) {
      return this.XIAN_YONG_TIAO_ZHANG
    } else if (text.indexOf('淘宝天猫跨境服务基础费') !== -1) {
      return this.KUA_JING_JI_CHU
    } else if (text.indexOf('淘宝天猫跨境服务增值费') !== -1) {
      return this.KUA_JING_ZENG_ZHI
    } else if (text.indexOf('出海增长计划中大件跨境服务增值费') !== -1) {
      return this.KUA_JING_DA_JIAN
    } else if (text.indexOf('淘特营销推广服务费') !== -1) {
      return this.TAO_TE
    } else if (text.indexOf('限时红包代商家垫付扣回') !== -1) {
      return this.XIAN_SHI
    } else if (text.indexOf('品牌新享淘宝新品营销') !== -1) {
      return this.XIN_PIN
    } else if (text.indexOf('品牌新享-淘宝营销托管') !== -1) {
      return this.XIN_XIANG_FU_WU
    } else if (text.indexOf('消费券代付资金扣回') !== -1) {
      return this.XIAO_FEI_QUAN
    } else if (text.indexOf('保证金管控资金使用') !== -1) {
      return this.GUAN_KONG
    } else if (text.indexOf('限时礼金软件服务费') !== -1) {
      return this.XIAN_SHI_LI_JIN
    } else if (text.indexOf('商家集运物流服务费') !== -1) {
      return this.JI_YUN_WU_LIU
    } else if (text.indexOf('商家集运中转操作费') !== -1) {
      return this.JI_YUN_CAO_ZUO_FEI
      // ---------------------
    } else if (text.indexOf('公益宝贝捐赠') !== -1) {
      return this.GONG_YI
    } else if (text.indexOf('卖家延迟发货赔付红包') !== -1) {
      return this.YAN_CHI_FA_HUO
    } else if (text.indexOf('虚假发货赔付红包') !== -1) {
      return this.XU_JIA_FA_HUO
    } else if (text.indexOf('淘宝物流轨迹异常红包') !== -1) {
      return this.WU_LIU_YI_CHANG
    } else if (text.indexOf('淘宝缺货赔付红包') !== -1) {
      return this.QUE_HUO
    } else if (text.indexOf('花呗分期免息营销') !== -1) {
      return this.HUA_BEI
    } else if (text.indexOf('淘宝物流轨迹超时红包') !== -1) {
      return this.WU_LIU_CHAO_SHI
    } else if (text.indexOf('延迟换货补偿红包') !== -1) {
      return this.YAN_CHI_HUAN_HUO
      // ---------------------
    } else if (text.indexOf('退款') !== -1) {
      return this.TUI_KUAN
    } else if (text.indexOf('支付宝转账小额打款') !== -1) { // 要在转账之前
      return this.DA_KUAN
    } else if (text.indexOf('转账') !== -1) {
      return this.ZHUAN_ZHANG
    } else if (text.indexOf('淘宝消费者保证金') !== -1) {
      return this.BAO_ZHENG_JIN
    } else if (text.indexOf('万相台无界版自动充值') !== -1) {
      return this.CHONG_ZHI
      // ---------------------
    } else { // 异常
      return this.OTHER
    }
  },
  num2text(num) {
    switch (num) {
      case this.FU_WU_FEI:
        return '服务费'
      case this.XIN_XIANG:
        return '品牌新享'
      case this.XIN_KE:
        return '新客礼金'
      case this.TI_YAN:
        return '体验提升'
      case this.TAO_JIN_BI:
        return '淘金币'
      case this.XIAN_YONG_HOU_FU:
        return '先用后付'
      case this.XIAN_YONG_TIAO_ZHANG:
        return '先用后付调账'
      case this.KUA_JING_JI_CHU:
        return '跨境基础费'
      case this.KUA_JING_ZENG_ZHI:
        return '跨境增值费'
      case this.KUA_JING_DA_JIAN:
        return '出海大件服务费'
      case this.TAO_TE:
        return '淘特服务费'
      case this.XIAN_SHI:
        return '限时红包'
      case this.XIN_PIN:
        return '新品礼金'
      case this.XIN_XIANG_FU_WU:
        return '新享服务费'
      case this.XIAO_FEI_QUAN:
        return '消费券代付'
      case this.GUAN_KONG:
        return '管控资金使用'
      case this.XIAN_SHI_LI_JIN:
        return '限时礼金'
      case this.JI_YUN_WU_LIU:
        return '集运物流'
      case this.JI_YUN_CAO_ZUO_FEI:
        return '集运操作费'

      case this.GONG_YI:
        return '公益宝贝捐赠'
      case this.YAN_CHI_FA_HUO:
        return '延迟发货赔付'
      case this.XU_JIA_FA_HUO:
        return '虚假发货赔付'
      case this.WU_LIU_YI_CHANG:
        return '物流异常赔付'
      case this.QUE_HUO:
        return '缺货赔付'
      case this.HUA_BEI:
        return '花呗服务费'
      case this.WU_LIU_CHAO_SHI:
        return '物流轨迹超时'
      case this.YAN_CHI_HUAN_HUO:
        return '延迟换货赔付'

      case this.TUI_KUAN:
        return '退款'
      case this.ZHUAN_ZHANG:
        return '转账'
      case this.BAO_ZHENG_JIN:
        return '保证金'
      case this.DA_KUAN:
        return '小额打款'
      case this.CHONG_ZHI:
        return '万相台充值'
      case this.ONLINE:
        return '在线支付'
    }
    return '异常'
  }
}

// 财务类型
export const FinanceType = {
  MARGIN: 1, // 保证金
  SHARE: 2, // 分账
  ONLINE: 3, // 在线支付
  TRANSFER: 4, // 转账
  REFUND: 5, // 退款
  OTHER: 6, // 其他

  DEDUCTION: 7, // 扣款
  COLLECTION: 8, // 交易收款
  CASH: 9, // 提现

  ERROR: 10, // 异常

  text2num(text) {
    if (text === '保证金') {
      return this.MARGIN
    } else if (text === '分账') {
      return this.SHARE
    } else if (text === '在线支付') {
      return this.ONLINE
    } else if (text === '转账') {
      return this.TRANSFER
    } else if (text === '退款') {
      return this.REFUND
    } else if (text === '其他') {
      return this.OTHER
    } else if (text === '扣款') {
      return this.DEDUCTION
    } else if (text === '交易收款') {
      return this.COLLECTION
    } else if (text === '提现') {
      return this.CASH
    } else { // 异常
      return this.ERROR
    }
  },
  num2text(num) {
    switch (num) {
      case this.MARGIN:
        return '保证金'
      case this.SHARE:
        return '分账'
      case this.ONLINE:
        return '在线支付'
      case this.TRANSFER:
        return '转账'
      case this.REFUND:
        return '退款'
      case this.OTHER:
        return '其他'
      case this.DEDUCTION:
        return '扣款'
      case this.COLLECTION:
        return '收款'
      case this.CASH:
        return '提现'
    }
    return '异常'
  },
  getList() {
    return [{
      id: this.SALE, name: '在售'
    }, {
      id: this.REMOVE, name: '下架'
    }, {
      id: this.DELETE, name: '删除'
    }]
  }
}

// 商品状态
export const GoodStatus = {
  SALE: 1, // 在售
  REMOVE: 2, // 下架
  DELETE: 3, // 删除
  OTHER: 4, // 异常

  text2num(text) {
    if (text === '在售') {
      return this.SALE
    } else if (text === '下架') {
      return this.REMOVE
    } else if (text === '删除') {
      return this.DELETE
    } else { // 异常
      return this.OTHER
    }
  },
  num2text(num) {
    switch (num) {
      case this.SALE:
        return '在售'
      case this.REMOVE:
        return '下架'
      case this.DELETE:
        return '删除'
    }
    return '异常'
  },
  getList() {
    return [{
      id: this.SALE, name: '在售'
    }, {
      id: this.REMOVE, name: '下架'
    }, {
      id: this.DELETE, name: '删除'
    }]
  }
}

// 商品类型
export const GoodType = {
  NORMAL: 1, // 商品
  GIFT: 2, // 赠品
  SUPPLEMENT: 3, // 补差价
  OTHER: 4, // 异常

  text2num(text) {
    if (text === '商品') {
      return this.NORMAL
    } else if (text === '赠品') {
      return this.GIFT
    } else if (text === '补差价') {
      return this.SUPPLEMENT
    } else { // 异常
      return this.OTHER
    }
  },
  num2text(num) {
    switch (num) {
      case this.NORMAL:
        return '商品'
      case this.GIFT:
        return '赠品'
      case this.SUPPLEMENT:
        return '补差价'
    }
    return '异常'
  },
  getList() {
    return [{
      id: this.NORMAL, name: '商品'
    }, {
      id: this.GIFT, name: '赠品'
    }, {
      id: this.SUPPLEMENT, name: '补差价'
    }]
  }
}

// 订单状态
export const OrderStatus = {
  SUCCESS: 1, // 交易成功
  CLOSE: 2, // 交易关闭
  SHIPPED: 3, // 已发货：卖家已发货，等待买家确认
  PAID: 4, // 未发货：买家已付款,等待卖家发货
  UNPAID: 5, // 未付款：等待买家付款
  OTHER: 6, // 异常

  text2num(text) {
    if (text === '交易成功') {
      return this.SUCCESS
    } else if (text === '交易关闭') {
      return this.CLOSE
    } else if (text === '卖家已发货，等待买家确认') {
      return this.SHIPPED
    } else if (text === '买家已付款,等待卖家发货') {
      return this.PAID
    } else if (text === '等待买家付款') {
      return this.UNPAID
    } else { // 异常
      return this.OTHER
    }
  },
  num2text(num) {
    switch (num) {
      case this.SUCCESS:
        return '交易成功'
      case this.CLOSE:
        return '交易关闭'
      case this.SHIPPED:
        return '卖家已发货，等待买家确认'
      case this.PAID:
        return '买家已付款，等待卖家发货'
      case this.UNPAID:
        return '等待买家付款'
    }
    return '异常'
  },
  getList() {
    return [{
      id: this.OTHER, name: '全部'
    }, {
      id: this.SUCCESS, name: '交易成功'
    }, {
      id: this.CLOSE, name: '交易关闭'
    }, {
      id: this.SHIPPED, name: '已发货'
    }, {
      id: this.PAID, name: '待发货'
    }, {
      id: this.UNPAID, name: '待付款'
    }]
  }
}

// 推广类型
export const PromotionType = {
  CAR: 1, // 直通车
  WHOLE: 2, // 全站
  PEOPLE: 3, // 人群
  PREPAYMENT: 4, // 下单金额被预支付扣款
  OTHER: 5, // 异常

  text2num(text) {
    if (text.indexOf('现金消耗扣款') !== -1) {
      return this.CAR
    } else if (text.indexOf('全站推消耗扣款') !== -1) {
      return this.WHOLE
    } else if (text.indexOf('人群超市订单') !== -1) {
      return this.PEOPLE
    } else if (text.indexOf('下单金额被预支付扣款') !== -1) {
      return this.PREPAYMENT
    } else { // 异常
      return this.OTHER
    }
  },
  num2text(num) {
    switch (num) {
      case this.CAR:
        return '直通车'
      case this.WHOLE:
        return '全站'
      case this.PEOPLE:
        return '人群'
      case this.PREPAYMENT:
        return '预支付扣款'
    }
    return '异常'
  }
}

// # 退货状态
export const RefundStatus = {
  SUCCESS: 1, // 退款成功
  CLOSE: 2, // 退款关闭
  APPLY: 3, // 买家已经申请退款，等待卖家同意
  AGREE: 4, // 卖家已经同意退款，等待买家退货
  SHIPPED: 5, // 买家已经退货，等待卖家确认收货
  EXCHANGE: 6, // 卖家已发货,等待卖家和买家确认收货
  AGAIN: 7, // 等待买家确认重新邮寄的货物
  REFUSE: 8, // 卖家拒绝退款
  OTHER: 9, // 异常

  text2num(text) {
    if (text === '退款成功') {
      return this.SUCCESS
    } else if (text === '退款关闭') {
      return this.CLOSE
    } else if (text === '买家已经申请退款，等待卖家同意') {
      return this.APPLY
    } else if (text === '卖家已经同意退款，等待买家退货') {
      return this.AGREE
    } else if (text === '买家已经退货，等待卖家确认收货') {
      return this.SHIPPED
    } else if (text === '卖家已发货,等待卖家和买家确认收货') {
      return this.EXCHANGE
    } else if (text === '等待买家确认重新邮寄的货物') {
      return this.AGAIN
    } else if (text === '卖家拒绝退款') {
      return this.REFUSE
    } else { // 异常
      return this.OTHER
    }
  },
  num2text(num) {
    switch (num) {
      case this.SUCCESS:
        return '退款成功'
      case this.CLOSE:
        return '退款关闭'
      case this.APPLY:
        return '买家已经申请退款，等待卖家同意'
      case this.AGREE:
        return '卖家已经同意退款，等待买家退货'
      case this.SHIPPED:
        return '买家已经退货，等待卖家确认收货'
      case this.EXCHANGE:
        return '卖家已发货,等待卖家和买家确认收货'
      case this.AGAIN:
        return '等待买家确认重新邮寄的货物'
      case this.REFUSE:
        return '卖家拒绝退款'
    }
    return '异常'
  }
}

// 退款状态
export const RefundType = {
  ONLY_REFUND: 1, // 仅退款
  RETURN: 2, // 退货退款
  EXCHANGE: 3, // 换货
  RESEND: 4, // 补寄
  REFUND: 5, // 退款
  SHIPPED: 6, // 退运费
  REPAIR: 7, // 维修
  DIFFERENCE: 8, // 邮费退差
  OTHER: 9, // 异常

  text2num(text) {
    if (text === '仅退款') {
      return this.ONLY_REFUND
    } else if (text === '退货退款') {
      return this.RETURN
    } else if (text === '换货') {
      return this.EXCHANGE
    } else if (text === '补寄') {
      return this.RESEND
    } else if (text === '退款') {
      return this.REFUND
    } else if (text === '退运费') {
      return this.SHIPPED
    } else if (text === '维修') {
      return this.REPAIR
    } else if (text === '邮费退差') {
      return this.DIFFERENCE
    } else { // 异常
      return this.OTHER
    }
  },
  num2text(num) {
    switch (num) {
      case this.ONLY_REFUND:
        return '仅退款'
      case this.RETURN:
        return '退货退款'
      case this.EXCHANGE:
        return '换货'
      case this.RESEND:
        return '补寄'
      case this.REFUND:
        return '退款'
      case this.SHIPPED:
        return '退运费'
      case this.REPAIR:
        return '维修'
      case this.DIFFERENCE:
        return '邮费退差'
    }
    return '异常'
  }
}
