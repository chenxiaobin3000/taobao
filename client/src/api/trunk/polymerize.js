import request from '@/utils/request'
const path = '/polymerize'

export function mergePolymerize(data) {
  return request({
    url: `${path}/merge`,
    method: 'post',
    data
  })
}

export function delPolymerize(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getPolymerizeList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
