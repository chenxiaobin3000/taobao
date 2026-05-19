import request from '@/utils/request'
const path = '/receipt_item'

export function addReceiptItem(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function setReceiptItem(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delReceiptItem(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getReceiptItemList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
