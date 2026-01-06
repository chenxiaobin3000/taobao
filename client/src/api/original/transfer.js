import request from '@/utils/request'
const path = '/transfer'

export function addTransfer(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function addTransferList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function setTransfer(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delTransfer(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getTransferList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
