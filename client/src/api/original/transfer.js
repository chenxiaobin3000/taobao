import request from '@/utils/request'
const path = '/user_transfer'

export function addUserTransferList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function delUserTransfer(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllUserTransfer(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getUserTransferList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
