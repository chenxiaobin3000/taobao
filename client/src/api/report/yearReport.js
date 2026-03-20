import request from '@/utils/request'
const path = '/year_report'

export function getYearReport(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
