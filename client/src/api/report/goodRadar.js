import request from '@/utils/request'
const path = '/good_rader'

export function getGoodRader(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
