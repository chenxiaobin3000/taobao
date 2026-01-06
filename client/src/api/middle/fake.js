import request from '@/utils/request'
const path = '/fake'

export function flushFake(data) {
  return request({
    url: `${path}/flush`,
    method: 'post',
    data
  })
}

export function setFake(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function getFakeList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
