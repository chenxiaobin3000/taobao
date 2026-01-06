import request from '@/utils/request'
const path = '/role'

export function addRole(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function setRole(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delRole(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getRole(data) {
  return request({
    url: `${path}/get`,
    method: 'post',
    data
  })
}

export function getRoleList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
