import request from '@/utils/request'
const path = '/receipt_to'

export function addReceiptTo(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data,
    timeout: 5000
  })
}

export function delReceiptTo(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getReceiptToList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
