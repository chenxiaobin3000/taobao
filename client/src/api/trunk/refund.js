import request from '@/utils/request'
const path = '/refund'

export function mergeRefund(data) {
  return request({
    url: `${path}/merge`,
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
