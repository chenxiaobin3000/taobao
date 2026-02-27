import request from '@/utils/request'
const path = '/user_polymerize_discard'

export function delPolymerizeDiscard(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllPolymerizeDiscard(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getPolymerizeDiscardList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
