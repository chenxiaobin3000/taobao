import request from '@/utils/request'
const path = '/misc'

export function addMisc(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function setMisc(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delMisc(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getMiscList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
