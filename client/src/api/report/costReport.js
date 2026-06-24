import request from '@/utils/request'
const path = '/cost_report'

export function getCostReport(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
