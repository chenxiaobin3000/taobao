import request from '@/utils/request'
const path = '/purchase_report'

export function getPurchaseReportList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
