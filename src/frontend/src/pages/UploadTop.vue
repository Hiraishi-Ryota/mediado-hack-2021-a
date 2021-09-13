<template>
  <div>
    <Header :color="color"></Header>

    <v-card
      class="mx-auto mt-15"
      max-width="500"
      outlined
    >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h5 my-8 text-center">
            epubデータのアップロード
          </v-list-item-title>
          <v-list-item-subtitle>以下の情報を入力してください。</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-list-item>
        <v-list-item-content>
          <label for="file" class="mb-2 font-weight-bold">epubデータ</label>
          <input type="file" id="file">
        </v-list-item-content>
      </v-list-item>

      <v-list-item>
        <v-list-item-content>
          <label for="price" class="mb-2 font-weight-bold">本の値段</label>
          <span><input type="number" id="price"> 円</span>
        </v-list-item-content>
      </v-list-item>

      <v-card-actions>
        <v-btn
          rounded
          color="orange"
          dark
          class="mx-auto my-5"
        >
          アップロード
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import Header from '../components/Header.vue'

export default {
  components: {
    Header
  },
  data() {
    return {
      color: 'orange'
    }
  }
}
</script>

<style scoped>
#price {
  border-bottom: 1px solid #000;
}
</style>