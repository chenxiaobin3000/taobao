import request from '@/utils/request'
const path = '/user'

export function addUser(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function setUser(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delUser(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getUser(data) {
  return request({
    url: `${path}/get`,
    method: 'post',
    data
  })
}

export function getUserInfo(data) {
  return request({
    url: `${path}/getInfo`,
    method: 'post',
    data
  })
}

export function getUserByPhone(data) {
  return request({
    url: `${path}/getByPhone`,
    method: 'post',
    data
  })
}

export function getUserList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
