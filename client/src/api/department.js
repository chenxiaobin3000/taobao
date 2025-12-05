import request from '@/utils/request'
const path = '/department'

export function addDepartment(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function setDepartment(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delDepartment(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getGroupDepartmentList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}

export function getGroupDepartmentTree(data) {
  return request({
    url: `${path}/getTree`,
    method: 'post',
    data
  })
}

export function setUserDepartment(data) {
  return request({
    url: `${path}/setUserDepartment`,
    method: 'post',
    data
  })
}
