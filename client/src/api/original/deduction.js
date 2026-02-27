import request from '@/utils/request'
const path = '/user_deduction'

export function addDeductionList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function delDeduction(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getDeductionList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
