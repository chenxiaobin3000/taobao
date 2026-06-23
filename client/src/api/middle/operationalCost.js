import request from '@/utils/request'

const path = '/operational_cost'

export function addOperationalCost(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function addOperationalCostList(data) {
  return request({
    url: `${path}/addList`,
    method: 'post',
    data
  })
}

export function setOperationalCost(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function delOperationalCost(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getOperationalCostList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
