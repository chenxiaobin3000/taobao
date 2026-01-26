import request from '@/utils/request'
const path = '/cost_report'

export function getCostReportList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
