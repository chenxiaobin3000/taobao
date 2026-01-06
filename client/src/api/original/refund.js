import request from '@/utils/request'
const path = '/refund'

export function addRefund(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function addRefundList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function setRefund(data) {
  return request({
    url: `${path}/set`,
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
