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
  ZHUANGZHANG: 200 // 转账
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
