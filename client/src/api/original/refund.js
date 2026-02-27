import request from '@/utils/request'
const path = '/user_refund'

export function addRefundList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function delRefund(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getRefundList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
