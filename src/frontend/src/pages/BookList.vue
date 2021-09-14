<template>
  <div>
    <Header :color="color"></Header>

    <v-container>
      <v-row>
        <v-col>
          <h2 class="text-center mt-8">本一覧</h2>
        </v-col>
      </v-row>

      <v-row class="mx-auto">
        <v-col
          xs="12"
          sm="4"
          md="4"
          lg="3"
          v-for="book in books"
          :key="book.id"
          @click="goToDetail(book.id)"
          class="book d-flex flex-column mb-5"
          v-ripple
          max-height="420"
        >
          <v-img 
            :src="book.cover_img"
            max-width="200"
            min-height="280"
            class="mx-auto"
            contain
          ></v-img>

          <v-list max-width="200" class="mx-auto">
            <v-list-item>
              <h3 class="mx-auto my-3">{{ book.title }}</h3>
            </v-list-item>

            <v-list-item>
              <p>
                著者：{{ book.author }}
                <br />
                値段：{{ book.price }}円
              </p>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import Header from '../components/Header.vue'

export default {
  components: {
    Header,
  },
  data() {
    return {
      color: 'primary',
      books: [
        {
          id: 1,
          title: '本の名前1',
          author: '著者1著者1',
          price: 1000,
          cover_img: '',
        },
        {
          id: 2,
          title: '本の名前2',
          author: '著者2',
          price: 1500,
          cover_img: '',
        },
        {
          id: 3,
          title: '本の名前3',
          author: '著者3',
          price: 5000,
          cover_img:
            'https://images-na.ssl-images-amazon.com/images/I/812NbfCwTvL.jpg',
        },
        {
          id: 4,
          title: '本の名前4',
          author: '著者4',
          price: 3000,
          cover_img: 'https://t.pimg.jp/073/204/498/1/73204498.jpg',
        },
        {
          id: 5,
          title: '本の名前5',
          author: '著者5',
          price: 10000,
          cover_img: 'https://www.abbeville.com/assets/common/images/edition_placeholder.png',
        },
      ],
    }
  },
  methods: {
    goToDetail(id) {
      this.$router.push(`/book_list/${id}`)
    },
  },
}
</script>

<style scoped>
.book {
  cursor: pointer;
  border-radius: 10px;
}

.book:hover {
  box-shadow: 1px 1px 12px rgba(0, 0, 0, 0.3);
}
</style>
