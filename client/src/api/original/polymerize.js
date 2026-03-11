import request from '@/utils/request'
const path = '/user_polymerize'

export function addUserPolymerizeList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function delUserPolymerize(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllUserPolymerize(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getUserPolymerizeList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
