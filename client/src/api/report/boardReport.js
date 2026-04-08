import request from '@/utils/request'
const path = '/board_report'

export function getBoardReport(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
