import request from '@/utils/request'
const path = '/user_promotion'

export function addUserPromotionList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function delUserPromotion(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function delAllUserPromotion(data) {
  return request({
    url: `${path}/delAll`,
    method: 'post',
    data
  })
}

export function getUserPromotionList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
