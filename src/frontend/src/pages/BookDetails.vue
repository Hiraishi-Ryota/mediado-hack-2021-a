<template>
  <div>
    <Header :color="color"></Header>
    <v-container>
      <v-col>
        <h1 class="text-center mt-8">{{ bookDetail.title }}</h1>
      </v-col>
      <v-row class="mb-5">
        <v-col cols="6" class="d-flex justify-center align-center">
          <v-img :src="bookDetail.cover_img" max-width="200" class="mx-auto">
          </v-img>
        </v-col>
        <v-col cols="4" class="d-flex justify-center align-center">
          <h3>
            著者：{{ bookDetail.author }}
            <p />
            値段：{{ bookDetail.price }}円
            <p />
            文字数：{{ bookDetail.word_count }}文字
          </h3>
        </v-col>
      </v-row>
      <v-row
        v-for="(chapter, index) in bookDetail.chapters"
        :key="chapter.id"
        class="my-5"
      >
        <v-col cols="2" class="d-flex justify-center align-center">
          <h3>{{ index + 1 }}章</h3>
        </v-col>
        <v-col cols="6" class="d-flex justify-center align-center">
          <h3>{{ chapter.title }}</h3>
        </v-col>
        <v-col cols="2" class="d-flex justify-center align-center">
          <h3>{{ chapter.price }}円</h3>
        </v-col>
        <v-col cols="2" class="d-flex justify-center align-center">
          <v-btn
            elevation="2"
            :ripple="false"
            color="orange"
            dark
            large
            rounded
            class="font-weight-bold"
            @click="gotoRead(chapter.e_pub, chapter.id)"
            >読む</v-btn
          >
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
    Header,
  },
  mounted: async function() {
    const bookId = this.$route.params['id']
    const res = await axios.get(`http://18.183.167.68/books/${bookId}`)
    this.bookDetail = res.data
    console.log(this.bookDetail)
  },
  data() {
    return {
      color: 'primary',
      bookDetail: {
        id: 1,
        title: 'ワンピース',
        price: 3000,
        author: '尾田栄一郎',
        cover_img:
          'https://images-na.ssl-images-amazon.com/images/I/812NbfCwTvL.jpg',
        e_pub: 'ワンピース',
        word_count: 1000,
        chapters: [
          {
            title: '1章のタイトル',
            price: 600,
            word_count: 100,
            e_pub: 'test',
            author: '尾田栄一郎',
            id: 1,
            book_id: 1,
          },
          {
            title: '2章のタイトル',
            price: 700,
            word_count: 100,
            e_pub: 'test',
            author: '尾田栄一郎',
            id: 2,
            book_id: 1,
          },
          {
            title: '3章のタイトル',
            price: 800,
            word_count: 100,
            e_pub: 'test',
            author: '尾田栄一郎',
            id: 3,
            book_id: 1,
          },
          {
            title: '4章のタイトル',
            price: 900,
            word_count: 100,
            e_pub: 'test',
            author: '尾田栄一郎',
            id: 4,
            book_id: 1,
          },
        ],
      },
    }
  },
  methods: {
    gotoRead: function(epub, chapterId) {
      console.log(chapterId)
      this.$router.push({
        path: `/read_screen/${this.$route.params['id']}/${chapterId}/${epub}`,
        params: {
          chapterId: chapterId,
        },
      })
    },
  },
}
</script>
