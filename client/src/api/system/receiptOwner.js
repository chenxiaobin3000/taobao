import request from '@/utils/request'
const path = '/receipt_owner'

export function addReceiptOwner(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function delReceiptOwner(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getReceiptOwnerList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
