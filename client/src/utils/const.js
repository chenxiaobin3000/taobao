// 扣款状态
export const DeductionType = {
  // 有订单信息
  FU_WU_FEI: 1, // 基础软件服务费
  XIN_XIANG: 2, // 品牌新享
  XIN_KE: 3,  // 淘宝新客礼金技术服务费
  TI_YAN: 4,  // 消费者体验提升计划服务费
  TAO_JIN_BI: 5,  // 淘金币软件服务费
  XIAN_YONG_HOU_FU: 6,  // 先用后付技术服务费()
  XIAN_YONG_TIAO_ZHANG: 7,  // 先用后付技术服务费-
  KUA_JING_JI_CHU: 8,  // 淘宝天猫跨境服务基础费
  KUA_JING_ZENG_ZHI: 9,  // 淘宝天猫跨境服务增值费
  KUA_JING_DA_JIAN: 10,  // 出海增长计划中大件跨境服务增值费
  TAO_TE: 11,  // 淘特营销推广服务费

  // 无订单信息
  GONG_YI: 100,  // 公益宝贝捐赠
  YAN_CHI_FA_HUO: 101,  // 卖家延迟发货赔付红包
  XU_JIA_FA_HUO: 102,  // 虚假发货赔付红包
  WU_LIU_YI_CHANG: 103,  // 淘宝物流轨迹异常红包
  QUE_HUO: 104,  // 淘宝缺货赔付红包
  HUA_BEI: 105,  // 花呗分期免息营销

  // 不处理
  ZHUANGZHANG: 200 // 转账
}

// 订单状态
export const OrderStatus = {
  SUCCESS: 1, // 交易成功
  CLOSE: 2,   // 交易关闭
  SHIPPED: 3, // 已发货：卖家已发货，等待买家确认
  PAID: 4,    // 未发货：买家已付款,等待卖家发货 5等待买家付款
  UNPAID: 5,  // 未付款：等待买家付款
  OTHER: 6,   // 异常
}

// # 退货状态
export const RefundStatus = {
  SUCCESS: 1, // 退款成功
  CLOSE: 2,   // 退款关闭
  SHIPPED: 3, // 买家已退货，等待卖家收货
  AGREE: 4,   // 卖家已同意，等待买家退货
  OTHER: 5  // 异常
}

// 退款状态
export const RefundType = {
  REFUND: 1, // 仅退款
  RETURN: 2, // 退货退款
  OTHER: 3  // 异常
}
