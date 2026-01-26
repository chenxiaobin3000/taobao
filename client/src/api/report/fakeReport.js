import request from '@/utils/request'
const path = '/fake_report'

export function getFakeReportList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
