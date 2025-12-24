import request from '@/utils/request'
const path = '/permission'

export function addPermission(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function setPermission(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delPermission(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getPermission(data) {
  return request({
    url: `${path}/get`,
    method: 'post',
    data
  })
}

export function getPermissionList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
