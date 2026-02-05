import request from '@/utils/request'
const path = '/deduction_summary'

export function flushDeductionSummary(data) {
  return request({
    url: `${path}/flush`,
    method: 'post',
    data
  })
}

export function getDeductionSummaryList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
