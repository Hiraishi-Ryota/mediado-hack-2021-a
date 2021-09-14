import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// ストアの定義
const store = new Vuex.Store({
  state: {
    purchasedItems: [-1],
  },
  getters: {
    getPurchasedItems(state) {
      return state.purchasedItems
    },
  },
  actions: {
    addIdAction({ commit }) {
      commit('addId')
    },
  },
  mutations: {
    addId(state, payload) {
      state.purchasedItems.push(payload)
    },
  },
})

// ストアをエクスポート
export default store
