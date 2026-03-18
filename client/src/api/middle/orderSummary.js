import request from '@/utils/request'
const path = '/order_summary'

export function flushOrderSummary(data) {
  return request({
    url: `${path}/flush`,
    method: 'post',
    data
  })
}

export function getOrderSummaryList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
