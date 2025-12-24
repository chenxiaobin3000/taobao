import request from '@/utils/request'
const path = '/good'

export function addGood(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function setGood(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delGood(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getGood(data) {
  return request({
    url: `${path}/get`,
    method: 'post',
    data
  })
}

export function getGoodList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
