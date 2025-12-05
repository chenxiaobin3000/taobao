import md5 from 'js-md5'
import { login, logout } from '@/api/account'
import { getUser } from '@/api/user'
import { setToken, getToken, removeToken, setUserId, getUserId, removeUserId } from '@/utils/cache'
import { resetRouter } from '@/router'

const state = {
  token: getToken(),
  id: getUserId(),
  roles: [],
  userdata: {}
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_ID: (state, id) => {
    state.id = id
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  },
  SET_USERDATA: (state, userdata) => {
    state.userdata = userdata
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { account, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ account: account.trim(), password: md5(password) }).then(response => {
        const { id, token } = response.data.data
        commit('SET_TOKEN', token)
        commit('SET_ID', id)
        commit('SET_ROLES', [])
        commit('SET_USERDATA', {})
        setUserId(id)
        setToken(token)
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getUser({ id: state.id }).then(response => {
        const { user, perms, market } = response.data.data
        // roles must be a non-empty array
        if (!perms || perms.length <= 0) {
          reject('账号权限被移除，无法登录，请联系系统管理员')
        }
        commit('SET_ROLES', perms)
        commit('SET_USERDATA', {
          user: user,
          market: market
        })
        resolve({
          name: user.name,
          roles: perms
        })
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state, dispatch }) {
    return new Promise((resolve, reject) => {
      logout({ id: state.id }).then(() => {
        commit('SET_TOKEN', '')
        commit('SET_ID', 0)
        commit('SET_ROLES', [])
        commit('SET_USERDATA', {})
        removeToken()
        removeUserId()
        resetRouter()

        // reset visited views and cached views
        dispatch('tagsView/delAllViews', null, { root: true })

        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  relogin({ commit, dispatch }) {
    return new Promise(resolve => {
      commit('SET_TOKEN', '')
      commit('SET_ID', 0)
      commit('SET_ROLES', [])
      commit('SET_USERDATA', {})
      removeToken()
      removeUserId()
      resetRouter()

      // reset visited views and cached views
      dispatch('tagsView/delAllViews', null, { root: true })

      resolve()
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit('SET_TOKEN', '')
      commit('SET_ID', 0)
      commit('SET_ROLES', [])
      commit('SET_USERDATA', {})
      removeToken()
      removeUserId()
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
