import request from '@/utils/request'
const path = '/purchase'

export function addPurchaseList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function setPurchase(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delPurchase(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getPurchaseList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
