<template>
  <div>
    <Header :color="color"></Header>

    <v-card 
      v-if="upload"
      class="mx-auto mt-15"
      max-width="500"
      outlined
    >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h5 my-5 text-center">
            epubデータのアップロード
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <div class="px-15">
        <v-list-item>
          <v-list-item-content>
            <v-list-item-subtitle>以下の情報を入力してください。</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-list-item class="mb-8">
          <v-list-item-content>
            <label for="file" class="mb-2 font-weight-bold">epubデータ</label>
            <input type="file" id="file">
          </v-list-item-content>
        </v-list-item>

        <v-list-item class="mb-8">
          <v-list-item-content>
            <label for="price" class="mb-2 font-weight-bold">本の値段</label>
            <span><input type="number" id="price"> 円</span>
          </v-list-item-content>
        </v-list-item>
      </div>

      <v-card-actions>
        <v-btn
          rounded
          color="orange"
          dark
          class="mx-auto mb-5"
          @click="uploadData"
        >
          アップロード
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-container v-else>
      <v-row>
        <v-col>
          <h2 class="text-center mt-8">アップロードした内容</h2>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="4" class="d-flex justify-center align-center">
          <v-header class="font-weight-bold">本のタイトル</v-header>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="bookTitle"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="4" class="d-flex justify-center align-center">
          <v-header class="font-weight-bold">著者</v-header>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="author"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="4" class="d-flex justify-center align-center">
          <v-header class="font-weight-bold">値段</v-header>
        </v-col>
        <v-col cols="2">
          <v-text-field
            v-model="price"
            suffix="円"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="4" class="d-flex justify-center align-center">
          <v-header class="font-weight-bold">章の内容</v-header>
        </v-col>
      </v-row>

      <v-row 
        v-for="(chapter, index) in chapters"
        :key="chapter.id"
      >
        <v-col cols="4" class="d-flex justify-center align-center">
          <v-header class="font-weight-bold">{{ index+1 }}章</v-header>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="chapter.title"
          ></v-text-field>
        </v-col>
        <v-col cols="2">
          <v-text-field
            v-model="chapter.price"
            suffix="円"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col class="d-flex justify-center">
          <v-btn
            rounded
            color="orange"
            dark
            class="my-5"
            x-large
            @click="registerData"
          >
            登録
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
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
      color: 'orange',
      upload: true,
      bookTitle: 'ワンピース',
      author: '尾田栄一郎',
      price: 3000,
      chapters: [
        {
          id: 1,
          title: '1章のタイトル',
          price: 600
        },
        {
          id: 2,
          title: '2章のタイトル',
          price: 800
        },
        {
          id: 3,
          title: '3章のタイトル',
          price: 900
        },
        {
          id: 4,
          title: '4章のタイトル',
          price: 700
        },
      ]
    }
  },
  methods: {
    uploadData() {
      // TODO: アップロード処理
      this.upload = false
    },
    registerData() {
      // TODO: 本の情報を登録する処理
      this.upload = true
    }
  }
}
</script>

<style scoped>
#price {
  border-bottom: 1px solid #000;
}
</style>