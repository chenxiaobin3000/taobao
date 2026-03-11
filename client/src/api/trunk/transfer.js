import request from '@/utils/request'
const path = '/transfer'

export function mergeTransfer(data) {
  return request({
    url: `${path}/merge`,
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
