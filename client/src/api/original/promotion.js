import request from '@/utils/request'
const path = '/promotion'

export function addPromotion(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function addPromotionList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function delPromotion(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getPromotionList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
