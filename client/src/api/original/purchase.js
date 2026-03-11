import request from '@/utils/request'
const path = '/user_purchase'

export function addUserPurchaseList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function setUserPurchase(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delUserPurchase(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllUserPurchase(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getUserPurchaseList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
