import request from '@/utils/request'
const path = '/good_follow'

export function addGoodFollow(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function setGoodFollow(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delGoodFollow(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getGoodFollowList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
