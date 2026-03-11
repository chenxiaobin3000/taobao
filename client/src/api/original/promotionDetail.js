import request from '@/utils/request'
const path = '/user_promotion_detail'

export function addUserPromotionDetailList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function delUserPromotionDetail(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllUserPromotionDetail(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getUserPromotionDetailList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
