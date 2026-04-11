import request from '@/utils/request'
const path = '/good'

export function addGoodList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function flushGood(data) {
  return request({
    url: `${path}/flush`,
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

export function getGoodList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
