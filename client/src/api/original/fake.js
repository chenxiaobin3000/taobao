import request from '@/utils/request'
const path = '/fake'

export function delFake(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getFakeList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
