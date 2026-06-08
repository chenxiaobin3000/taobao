import request from '@/utils/request'
const path = '/receipt_manager'

export function getReceiptManagerList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
