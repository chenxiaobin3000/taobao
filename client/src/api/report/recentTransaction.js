import request from '@/utils/request'
const path = '/recent_transaction'

export function getRecentTransactionList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
