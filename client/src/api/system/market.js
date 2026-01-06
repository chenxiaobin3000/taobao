import request from '@/utils/request'
const path = '/market'

export function addMarket(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function setMarket(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delMarket(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getMarket(data) {
  return request({
    url: `${path}/get`,
    method: 'post',
    data
  })
}

export function getMarketList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
