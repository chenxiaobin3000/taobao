import request from '@/utils/request'
const path = '/shop'

export function addShop(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function setShop(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delShop(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getShop(data) {
  return request({
    url: `${path}/get`,
    method: 'post',
    data
  })
}

export function getShopList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
