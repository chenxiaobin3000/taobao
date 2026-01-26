import request from '@/utils/request'
const path = '/good_rader'

export function getGppdRaderList(data) {
  return request({
    url: `${path}/getList`,
    method: 'post',
    data
  })
}
