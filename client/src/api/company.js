import request from '@/utils/request'
const path = '/company'

export function addCompany(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function setCompany(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delCompany(data) {
  return request({
    url: `${path}/delete`,
    method: 'post',
    data
  })
}

export function getCompany(data) {
  return request({
    url: `${path}/get`,
    method: 'post',
    data
  })
}

export function getCompanyList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
