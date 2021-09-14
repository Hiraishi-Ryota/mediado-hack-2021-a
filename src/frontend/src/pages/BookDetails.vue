<template>
  <div>
    <Header :color="color"></Header>
    <v-container>
      <v-btn
        elevation="2"
        :ripple="false"
        color="primary"
        dark
        large
        rounded
        class="font-weight-bold"
        @click="gotoBack"
        >一覧へ戻る</v-btn
      >
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
            v-if="purchasedItems.includes(chapter.id)"
            elevation="2"
            :ripple="false"
            color="orange"
            dark
            large
            rounded
            class="font-weight-bold"
            @click="gotoRead(chapter.e_pub)"
            >読む</v-btn
          >
          <v-btn
            v-else
            elevation="2"
            :ripple="false"
            color="primary"
            dark
            large
            rounded
            class="font-weight-bold"
            @click="purchase(chapter.id)"
            >購入</v-btn
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
      bookDetail: {},
    }
  },
  computed: {
    purchasedItems() {
      return this.$store.getters['getPurchasedItems']
    },
  },
  methods: {
    purchase: function(chapterId) {
      this.$store.commit('addId', chapterId)
      alert('購入に成功しました！')
    },
    gotoBack: function() {
      this.$router.push({
        path: `/book_list`,
      })
    },
    gotoRead: function(epub, chapterId) {
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
