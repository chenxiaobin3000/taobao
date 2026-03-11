import request from '@/utils/request'
const path = '/user_deduction'

export function addUserDeductionList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function delUserDeduction(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllUserDeduction(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getUserDeductionList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
