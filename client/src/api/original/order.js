import request from '@/utils/request'
const path = '/user_order'

export function addUserOrderList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function delUserOrder(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllUserOrder(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getUserOrderList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
