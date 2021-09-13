<template>
  <div>
    <v-btn elevation="2" :ripple="false" @click="dialog = true"
      >詳細へ戻る</v-btn
    >
    <a
      :href="bibiLink"
      data-bibi="embed"
      data-bibi-style="width: 100%; height: 1000px;"
    ></a>
    <script2 src="http://localhost:8000/static/bibi/and/jo.js"></script2>

    <v-dialog v-model="dialog" scrollable max-width="80%">
      <v-card>
        <v-card-title>お勧めの章</v-card-title>
        <v-divider></v-divider>
        <v-col class="d-flex justify-center">
          <v-btn elevation="2" :ripple="false" @click="gotoDetails"
            >詳細へ戻る</v-btn
          >
        </v-col>
      </v-card>
    </v-dialog>
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
      dialog: false,
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
      return `http://localhost:8000/static/bibi/index.html?book=${this.title}.epub`
    },
  },
  methods: {
    gotoDetails: function() {
      this.$router.push({
        path: '/book_details/1',
      })
    },
  },
}
</script>

<style scoped></style>
