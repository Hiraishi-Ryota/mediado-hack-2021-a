<template>
  <div>
    <Header :color="color"></Header>

    <v-alert v-if="success" type="success" dismissible>
      本の情報を登録しました
    </v-alert>

    <!-- アップロード画面 -->
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
            <input type="file" id="file" @change="onImageUploaded">
          </v-list-item-content>
        </v-list-item>

        <v-list-item class="mb-8">
          <v-list-item-content>
            <label for="price" class="mb-2 font-weight-bold">本の値段</label>
            <span><input type="number" id="price" v-model="price"> 円</span>
          </v-list-item-content>
        </v-list-item>
      </div>

      <v-card-actions>
        <v-btn
          rounded
          :loading="loading1"
          color="orange"
          dark
          class="mx-auto mb-5"
          @click="uploadData"
        >
          アップロード
          <v-icon
            right
            dark
          >
            mdi-cloud-upload
          </v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- アップロード内容確認画面 -->
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
            v-model="confirmPrice"
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
        :key="index"
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
            :loading="loading2"
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
import axios from 'axios'

export default {
  components: {
    Header
  },
  data() {
    return {
      color: 'orange',
      success: false,
      upload: true,
      loading1: false,
      loading2: false,
      bookTitle: '',
      author: '',
      confirmPrice: 0,
      coverImg: '',
      wordCount: 0,
      ePub: '',
      chapters: [],
      price: 0,
      file: null
    }
  },
  methods: {
    onImageUploaded(e) {
      const files = e.target.files
      this.file = files[0]
    },
    async uploadData() {
      this.success = false

      this.loading1 = true
      
      let form = new FormData()
      form.append("e_pub", this.file);
      form.append("price", this.price);

      const config = {
        headers: {
          'content-type': 'multipart/form-data'
        }
      }

      const response = await axios.post('http://18.183.167.68/books/', form, config)

      this.bookTitle = response.data.title
      this.author = response.data.author
      this.confirmPrice = response.data.price
      this.coverImg = response.data.cover_img
      this.wordCount = response.data.word_count
      this.ePub = response.data.e_pub
      this.chapters = response.data.chapters

      this.loading1 = false

      this.upload = false

      this.price = 0
    },
    async registerData() {
      const data = {
        title: this.bookTitle,
        price: this.confirmPrice,
        author: this.author,
        e_pub: this.ePub,
        word_count: this.wordCount,
        cover_img: this.coverImg,
        chapters: this.chapters
      }

      this.loading2 = true

      const response = await axios.post('http://18.183.167.68/books/confirm', data)

      console.log(response.data)

      this.loading2 = false
      
      this.success = true
       
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