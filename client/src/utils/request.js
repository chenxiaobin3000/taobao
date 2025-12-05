import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import router from '@/router'
import { getToken } from '@/utils/cache'

function fixUrl(url) {
  const protocol = document.location.protocol
  if (protocol === 'http:') {
    return 'http://' + url
  } else if (protocol === 'https:') {
    return 'https://' + url
  }
}

// create an axios instance
const service = axios.create({
  baseURL: fixUrl(process.env.VUE_APP_BASE_API), // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    if (store.getters.token) {
      // 附加登录信息
      config.headers['token'] = getToken()
    }
    return config
  },
  error => {
    // do something with request error
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */
  response => {
    const res = response.data
    if (res.code !== 0) {
      if (res.code === -3) {
        MessageBox.confirm(res.msg, '确定登出', {
          confirmButtonText: '重新登陆',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          store.dispatch('account/relogin').then(() => {
            router.push('/login')
          })
        })
      } else {
        Message({
          message: res.msg,
          type: 'error',
          duration: 2000
        })
      }
      return Promise.reject(res.msg)
    } else {
      return response
    }
  },
  error => {
    const status = error.response.status
    if (status === 400) {
      Message({
        message: error.response.data.msg,
        type: 'error',
        duration: 2000
      })
    } else {
      Message({
        message: '网络异常，请联系客服',
        type: 'error',
        duration: 2000
      })
    }
    return Promise.reject(error)
  }
)

export default service
