<template>
  <div>
    <Header :color="color"></Header>
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