import request from '@/utils/request'
const path = '/omission_report'

export function getOmissionReport(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
