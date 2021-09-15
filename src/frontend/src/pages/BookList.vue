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
            height="280"
            class="mx-auto"
            contain
            v-on:error="
              () => (book.cover_img = require('@/assets/coming_soon.png'))
            "
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
import axios from 'axios'

export default {
  components: {
    Header,
  },
  data() {
    return {
      color: 'primary',
      books: [],
    }
  },
  mounted: async function() {
    const resBooks = await axios.get('http://18.183.167.68/books/')

    this.books = resBooks.data
    console.log(this.books)
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
