<template>
  <div class="main">
    <div class="fullheight">
      <a
        href="http://localhost:8000/static/bibi/index.html?book=test.epub"
        data-bibi="embed"
        data-bibi-style="width: 100%; height: 1000px;"
        >マイ・グレート・コミック</a
      >
      <script2 src="http://localhost:8000/static/bibi/and/jo.js"></script2>
      <!-- <script src="http://localhost:8000/static/bibi/and/jo.js"></script> -->
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import VS2 from 'vue-script2'

Vue.use(VS2)
export default {}
</script>

<style scoped>
main {
  height: 100%;
  margin: 0;
}

.fullheight {
  height: 100%;
}
</style>
