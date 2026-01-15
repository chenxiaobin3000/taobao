// 默认空时间
export const NoneTime = '2000-01-01 00:00:00'

// 批次导入数量
export const ImportCount = 1000

// 导入间隔时间
export const ImportSpan = 1000

// 扣款状态
export const DeductionType = {
  // 有订单信息
  FU_WU_FEI: 1, // 基础软件服务费
  XIN_XIANG: 2, // 品牌新享
  XIN_KE: 3, // 淘宝新客礼金技术服务费
  TI_YAN: 4, // 消费者体验提升计划服务费
  TAO_JIN_BI: 5, // 淘金币软件服务费
  XIAN_YONG_HOU_FU: 6, // 先用后付技术服务费()
  XIAN_YONG_TIAO_ZHANG: 7, // 先用后付技术服务费-
  KUA_JING_JI_CHU: 8, // 淘宝天猫跨境服务基础费
  KUA_JING_ZENG_ZHI: 9, // 淘宝天猫跨境服务增值费
  KUA_JING_DA_JIAN: 10, // 出海增长计划中大件跨境服务增值费
  TAO_TE: 11, // 淘特营销推广服务费

  // 无订单信息
  GONG_YI: 100, // 公益宝贝捐赠
  YAN_CHI_FA_HUO: 101, // 卖家延迟发货赔付红包
  XU_JIA_FA_HUO: 102, // 虚假发货赔付红包
  WU_LIU_YI_CHANG: 103, // 淘宝物流轨迹异常红包
  QUE_HUO: 104, // 淘宝缺货赔付红包
  HUA_BEI: 105, // 花呗分期免息营销

  // 不处理
  TUI_KUAN: 200, // 退款
  ZHUAN_ZHANG: 201, // 转账
  OTHER: 1000, // 异常

  text2num(text) {
    if (text.indexOf('基础软件服务费') !== -1) {
      return [this.FU_WU_FEI, this.match(text, '(', ')')]
    } else if (text.indexOf('品牌新享') !== -1) {
      return this.XIN_XIANG
    } else if (text.indexOf('淘宝新客礼金技术服务费') !== -1) {
      return this.XIN_KE
    } else if (text.indexOf('消费者体验提升计划服务费') !== -1) {
      return this.TI_YAN
    } else if (text.indexOf('淘金币软件服务费') !== -1) {
      return this.TAO_JIN_BI
    } else if (text.indexOf('先用后付技术服务费()') !== -1) {
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
    } else if (text.indexOf('退款') !== -1) {
      return this.TUI_KUAN
    } else if (text.indexOf('转账') !== -1) {
      return this.ZHUAN_ZHANG
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

      case this.TUI_KUAN:
        return '退款'
      case this.ZHUAN_ZHANG:
        return this.ZHUAN_ZHANG
    }
    return '异常'
  },
  match(text, symbol1, symbol2) {
    const first = text.indexOf(symbol1)
    if (first === -1) {
      return ''
    }
    const second = text.indexOf(symbol2, first + 1)
    if (second === -1) {
      return ''
    }
    return text.slice(first + 1, second)
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
  }
}

// 推广类型
export const PromotionType = {
  CAR: 1, // 直通车
  WHOLE: 2, // 全站
  PEOPLE: 3, // 人群
  OTHER: 4, // 异常

  text2num(text) {
    if (text.indexOf('现金消耗扣款') !== -1) {
      return this.CAR
    } else if (text.indexOf('全站推消耗扣款') !== -1) {
      return this.WHOLE
    } else if (text.indexOf('人群超市订单') !== -1) {
      return this.PEOPLE
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
  OTHER: 8, // 异常

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
    }
    return '异常'
  }
}

// 退款状态
export const RefundType = {
  REFUND: 1, // 仅退款
  RETURN: 2, // 退货退款
  OTHER: 3, // 异常

  text2num(text) {
    if (text === '退款') {
      return this.REFUND
    } else if (text === '退货退款') {
      return this.RETURN
    } else { // 异常
      return this.OTHER
    }
  },
  num2text(num) {
    switch (num) {
      case this.REFUND:
        return '仅退款'
      case this.RETURN:
        return '退货退款'
    }
    return '异常'
  }
}
