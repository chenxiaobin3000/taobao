import request from '@/utils/request'
const path = '/promotion_report'

export function getPromotionReport(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
