<template>
  <div>
    <script2 src="http://18.183.167.68/static/bibi/and/jo.js"></script2>
    <a
      :href="bibiLink"
      data-bibi="embed"
      data-bibi-style="width: 100%; height: 1000px;"
    ></a>
    <v-dialog v-model="dialog" width="50%">
      <v-card class="py-2">
        <v-card-title>こちらの商品もどうでしょうか？</v-card-title>
        <v-divider></v-divider>
        <v-row
          v-for="recommendItem in recommendItems"
          :key="recommendItem.id"
          class="d-flex justify-center align-center my-4"
        >
          <v-col cols="8" class="mx-4 d-flex  justify-start">
            <h4>{{ recommendItem.book_title }}</h4>
          </v-col>
          <v-col cols="6" class="d-flex align-center mx-4">
            <h2>{{ recommendItem.chapter_num }}章：</h2>

            <h2>{{ recommendItem.title }}</h2>
          </v-col>

          <v-col cols="2" class="d-flex justify-center align-center">
            <v-btn
              elevation="2"
              :ripple="false"
              color="primary"
              large
              rounded
              @click="
                () => gotoDetails(recommendItem.book_id, recommendItem.id)
              "
              >本の詳細へ</v-btn
            >
          </v-col>
        </v-row>
        <v-col class="d-flex justify-center ">
          <v-btn
            elevation="2"
            :ripple="false"
            @click="() => gotoDetails(bookId, chapterId)"
            >詳細へ戻る</v-btn
          >
        </v-col>
      </v-card>
    </v-dialog>
    <v-btn
      elevation="2"
      :ripple="false"
      @click="dialog = true"
      class="backButton"
      ><h2>詳細へ戻る</h2></v-btn
    >
  </div>
</template>

<script>
import Vue from 'vue'
import VS2 from 'vue-script2'
import axios from 'axios'

Vue.use(VS2)
export default {
  props: {
    // 本のid
    bookId: { type: String, default: '0' },
    // 章のid
    chapterId: { type: String, default: '0' },
    // 本のタイトル
    epubFileName: { type: String, default: 'hogehoge' },
  },
  data() {
    return {
      // モーダルを表示するか判定するフラグ
      dialog: false,
      recommendItems: [],
    }
  },
  mounted: async function() {
    // 1度だけ再読み込み
    if (window.name != 'any') {
      location.reload()
      window.name = 'any'
    } else {
      window.name = ''
    }
    const chapterId = this.$route.params['chapterId']
    const res = await axios.get(
      `http://18.183.167.68/chapters/recommend/${chapterId}`
    )
    this.recommendItems = res.data
    console.log(this.recommendItems)
  },
  computed: {
    bibiLink: function() {
      return `http://18.183.167.68/static/bibi/index.html?book=${this.epubFileName}`
    },
  },
  methods: {
    gotoDetails: function(bookId, chapterId) {
      this.$store.commit('addRecommendId', chapterId)
      this.$router.push({
        path: `/book_list/${bookId}`,
      })
    },
  },
}
</script>

<style scoped>
.backButton {
  position: fixed;
  top: 0;
  left: 0;
}
</style>
