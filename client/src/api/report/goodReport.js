import request from '@/utils/request'
const path = '/good_report'

export function getGoodReport(data) {
  return request({
    url: `${path}/get`,
    method: 'post',
    data
  })
}
