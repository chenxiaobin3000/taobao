import Cookies from 'js-cookie'

const CacheToken = 'store_token'
const CacheUserId = 'store_id'
const CacheAccount = 'store_account'
const CachePassword = 'store_pwd'

export function getToken() {
  return Cookies.get(CacheToken)
}

export function setToken(token) {
  Cookies.set(CacheToken, token)
}

export function removeToken() {
  Cookies.remove(CacheToken)
}

export function getUserId() {
  return Cookies.get(CacheUserId)
}

export function setUserId(id) {
  Cookies.set(CacheUserId, id)
}

export function removeUserId() {
  Cookies.remove(CacheUserId)
}

export function getAccount() {
  return Cookies.get(CacheAccount)
}

export function setAccount(account) {
  Cookies.set(CacheAccount, account)
}

export function removeAccount() {
  Cookies.remove(CacheAccount)
}

export function getPassword() {
  return Cookies.get(CachePassword)
}

export function setPassword(password) {
  Cookies.set(CachePassword, password)
}

export function removePassword() {
  Cookies.remove(CachePassword)
}
