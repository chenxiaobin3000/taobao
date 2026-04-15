import request from '@/utils/request'
const path = '/good_prepare'

export function addGoodPrepare(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function flushGoodPrepare(data) {
  return request({
    url: `${path}/flush`,
    method: 'post',
    data
  })
}

export function delGoodPrepare(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getGoodPrepareList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
