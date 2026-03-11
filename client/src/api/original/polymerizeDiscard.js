import request from '@/utils/request'
const path = '/user_polymerize_discard'

export function delUserPolymerizeDiscard(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllUserPolymerizeDiscard(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getUserPolymerizeDiscardList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
