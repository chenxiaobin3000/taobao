import request from '@/utils/request'
const path = '/good_radar'

export function getGoodRadar(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
