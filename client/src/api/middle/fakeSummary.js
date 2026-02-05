import request from '@/utils/request'
const path = '/fake_summary'

export function flushFakeSummary(data) {
  return request({
    url: `${path}/flush`,
    method: 'post',
    data
  })
}

export function setFakeSummary(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function getFakeSummaryList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
