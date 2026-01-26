import request from '@/utils/request'
const path = '/order_report'

export function flush(data) {
  return request({
    url: `${path}/flush`,
    method: 'post',
    data
  })
}
