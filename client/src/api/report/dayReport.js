import request from '@/utils/request'
const path = '/day_report'

export function getDayReport(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
