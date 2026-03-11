import request from '@/utils/request'
const path = '/user_fake'

export function delUserFake(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllUserFake(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getUserFakeList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
