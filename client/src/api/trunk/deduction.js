import request from '@/utils/request'
const path = '/deduction'

export function mergeDeduction(data) {
  return request({
    url: `${path}/merge`,
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
