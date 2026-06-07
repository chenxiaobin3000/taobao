import request from '@/utils/request'
const path = '/tax_report'

export function getTaxReport(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
