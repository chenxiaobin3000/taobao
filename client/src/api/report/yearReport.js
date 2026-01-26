import request from '@/utils/request'
const path = '/yesr_report'

export function getYearReportList(data) {
  return request({
    url: `${path}/get`,
    method: 'post',
    data
  })
}
