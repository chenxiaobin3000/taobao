import request from '@/utils/request'
const path = '/user_refund'

export function addUserRefundList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function delUserRefund(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllUserRefund(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getUserRefundList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
