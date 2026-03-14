import request from '@/utils/request'
const path = '/fake_report'

export function getFakeReport(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
