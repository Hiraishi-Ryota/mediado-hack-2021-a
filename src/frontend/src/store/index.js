import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// ストアの定義
const store = new Vuex.Store({
  state: {
    purchasedItems: 'hogehoge',
  },
  getters: {
    getPurchasedItems(state) {
      return state.purchasedItems
    },
  },
})

// ストアをエクスポート
export default store
