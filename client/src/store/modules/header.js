const state = {
  search: '', // 搜索
  shop: 0 // 当前店铺
}

const mutations = {
  SET_HEADER_SEARCH: (state, search) => {
    state.search = search
  },
  SET_HEADER_SHOP: (state, shop) => {
    state.shop = shop
  }
}

const actions = {
  search({ commit }, search) {
    commit('SET_HEADER_SEARCH', search)
  },
  shop({ commit }, shop) {
    commit('SET_HEADER_SHOP', shop)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
