import request from '@/utils/request'
const path = '/receipt_from'

export function addReceiptFrom(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data,
    timeout: 120000
  })
}

export function delReceiptFrom(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getReceiptFromList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
