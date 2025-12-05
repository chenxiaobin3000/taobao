const state = {
  search: '', // 搜索
  create: false // 新增
}

const mutations = {
  SET_HEADER_SEARCH: (state, search) => {
    state.search = search
  },
  SET_HEADER_CREATE: (state) => {
    state.create = !state.create
  }
}

const actions = {
  search({ commit }, search) {
    commit('SET_HEADER_SEARCH', search)
  },
  create({ commit }) {
    commit('SET_HEADER_CREATE')
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
