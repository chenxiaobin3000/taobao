import request from '@/utils/request'
const path = '/promotion_detail'

export function addPromotionDetail(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function addPromotionDetailList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function delPromotionDetail(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getPromotionDetailList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
