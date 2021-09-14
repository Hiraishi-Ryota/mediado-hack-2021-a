<template>
  <div>
    <script2 src="http://18.183.167.68/static/bibi/and/jo.js"></script2>
    <a
      :href="bibiLink"
      data-bibi="embed"
      data-bibi-style="width: 100%; height: 1000px;"
    ></a>
    <v-dialog v-model="dialog" width="80%">
      <v-card class="py-2">
        <v-card-title>こちらの商品もどうでしょうか？</v-card-title>
        <v-divider></v-divider>
        <v-row
          v-for="recommendItem in recommendItems"
          :key="recommendItem.bookId + recommendItem.chapterId"
          class="d-flex justify-center align-center my-4"
        >
          <v-col cols="8" class="mx-4 d-flex  justify-start">
            <h4>{{ recommendItem.bookTitle }}</h4>
          </v-col>
          <v-col cols="6" class="d-flex align-center mx-4">
            <h2>{{ recommendItem.chapterId }}章：</h2>

            <h2>{{ recommendItem.chapterTitle }}</h2>
          </v-col>

          <v-col cols="2" class="d-flex justify-center align-center">
            <v-btn
              elevation="2"
              :ripple="false"
              @click="() => gotoDetails(recommendItem.bookId)"
              >詳細</v-btn
            >
          </v-col>
        </v-row>
        <v-col class="d-flex justify-center ">
          <v-btn elevation="2" :ripple="false" @click="() => gotoDetails(id)"
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

Vue.use(VS2)
export default {
  props: {
    //本のid
    id: { type: String, default: '0' },
    //本のタイトル
    title: { type: String, default: 'hogehoge' },
  },
  data() {
    return {
      // モーダルを表示するか判定するフラグ
      dialog: false,
      recommendItems: [
        {
          bookTitle: '本のタイトル',
          bookId: 1,
          author: '著者名',
          chapterTitle: '章のタイトル',
          chapterId: 1,
          chapterPrice: 1000,
          word_count: 10000,
        },
        {
          bookTitle: '本2のタイトル',
          bookId: 2,
          author: '著者名2',
          chapterTitle: '章のタイトル2',
          chapterId: 1,
          chapterPrice: 1000,
          word_count: 10000,
        },
      ],
    }
  },
  mounted: function() {
    // 1度だけ再読み込み
    if (window.name != 'any') {
      location.reload()
      window.name = 'any'
    } else {
      window.name = ''
    }
  },
  computed: {
    bibiLink: function() {
      return `http://18.183.167.68/static/bibi/index.html?book=${this.title}.epub`
    },
  },
  methods: {
    gotoDetails: function(bookId) {
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
