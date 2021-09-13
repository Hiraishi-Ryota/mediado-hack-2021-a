<template>
  <div>
    本詳細画面
    <v-btn elevation="2" :ripple="false" @click="gotoRead()"
      >この章を読む</v-btn
    >
  </div>
</template>

<script>
export default {
  data() {
    return {
      title: 'test',
    }
  },
  methods: {
    gotoRead: function() {
      this.$router.push({
        path: `/read_screen/${this.$route.params['id']}/${this.title}`,
      })
    },
  },
}
</script>
