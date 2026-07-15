import request from '@/utils/request'
const path = '/good_prepare_record'

export function getGoodPrepareRecordList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}

export function setGoodPrepareRecord(data) {
  return request({
    url: `${path}/set`,
    method: 'post',
    data
  })
}

export function clearGoodPrepareRecord(data) {
  return request({
    url: `${path}/clear`,
    method: 'post',
    data
  })
}
