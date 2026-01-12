import request from '@/utils/request'
const path = '/good_alias'

export function addGoodAlias(data) {
  return request({
    url: `${path}/add`,
    method: 'post',
    data
  })
}

export function getGoodAliasById(data) {
  return request({
    url: `${path}/getById`,
    method: 'post',
    data
  })
}

export function getGoodAliasByName(data) {
  return request({
    url: `${path}/getByName`,
    method: 'post',
    data
  })
}

export function delGood(data) {
  return request({
    url: `${path}/del`,
    method: 'post',
    data
  })
}

export function getGoodList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
