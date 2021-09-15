import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

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
  plugins: [
    // 参考:https://qiita.com/_masa_u/items/b58b92c283f4e770e094
    createPersistedState({
      // ストレージのキーを指定。デフォルトではvuex
      key: 'anyGreatApp',

      // ストレージの種類を指定する。セッションが切れたらorタブやブラウザを閉じたらリセット
      storage: window.sessionStorage,
    }),
  ],
})

// ストアをエクスポート
export default store
