import request from '@/utils/request'
const path = '/storage'

export function addStorage(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function setStorage(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delStorage(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getGroupStorage(data) {
  return request({
    url: `${path}/get`,
    method: 'post',
    data
  })
}

export function getGroupAllStorage(data) {
  return request({
    url: `${path}/getAll`,
    method: 'post',
    data
  })
}
