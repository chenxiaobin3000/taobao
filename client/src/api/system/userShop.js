import request from '@/utils/request'
const path = '/userShop'

export function addUserShop(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function delUserShop(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getUserShopList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
