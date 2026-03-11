import request from '@/utils/request'
const path = '/user_refund_gift'

export function delUserRefundGift(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllUserRefundGift(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getUserRefundGiftList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
