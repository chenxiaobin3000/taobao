import request from '@/utils/request'
const path = '/user_deduction_discard'

export function delUserDeductionDiscard(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllUserDeductionDiscard(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getUserDeductionDiscardList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
