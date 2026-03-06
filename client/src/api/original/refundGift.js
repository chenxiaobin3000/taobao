import request from '@/utils/request'
const path = '/user_refund_gift'

export function delRefundGift(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllRefundGift(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getRefundGiftList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
