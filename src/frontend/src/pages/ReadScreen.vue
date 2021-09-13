<template>
  <div>
    <v-btn elevation="2" :ripple="false">詳細へ戻る</v-btn>
    {{ title }}
    <a
      :href="bibiLink"
      data-bibi="embed"
      data-bibi-style="width: 100%; height: 1000px;"
    ></a>
    <script2 src="http://localhost:8000/static/bibi/and/jo.js"></script2>
  </div>
</template>

<script>
import Vue from 'vue'
import VS2 from 'vue-script2'

Vue.use(VS2)
export default {
  props: {
    title: { type: String, default: 'hogehoge' },
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
}
</script>

<style scoped></style>
