<template>
  <div>
    <Header :color="color"></Header>
    
    <v-container>
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
    registerData() {
      // TODO: 本の情報を登録する処理
      this.$router.push('/')
    }
  }
}
</script>
