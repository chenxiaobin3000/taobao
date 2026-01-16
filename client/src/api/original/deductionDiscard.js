import request from '@/utils/request'
const path = '/deduction_discard'

export function delDeductionDiscard(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllDeductionDiscard(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getDeductionDiscardList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
