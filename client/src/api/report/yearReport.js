import request from '@/utils/request'
const path = '/yesr_report'

export function getYearReport(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
