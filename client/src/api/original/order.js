import request from '@/utils/request'
const path = '/order'

export function addOrderList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function delOrder(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getOrderList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
