import request from '@/utils/request'
const path = '/account'

export function register(data) {
  return request({
    url: `${path}/register`,
    method: 'post',
    data
  })
}

export function login(data) {
  return request({
    url: `${path}/login`,
    method: 'post',
    data
  })
}

export function logout(data) {
  return request({
    url: `${path}/logout`,
    method: 'post',
    data
  })
}

export function setPassword(data) {
  return request({
    url: `${path}/setPassword`,
    method: 'post',
    data
  })
}

export function resetPwd(data) {
  return request({
    url: `${path}/resetPwd`,
    method: 'post',
    data
  })
}
