<template>
  <div>
    本詳細画面
    <v-btn elevation="2" :ripple="false" @click="gotoRead()"></v-btn>
  </div>
</template>

<script>
export default {
  methods: {
    gotoRead: function() {
      console.log('test')
      this.$router.push({
        path: '/read_screen/test',
      })
    },
  },
}
</script>
