import request from '@/utils/request'
const path = '/promotion'

export function mergePromotion(data) {
  return request({
    url: `${path}/merge`,
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
