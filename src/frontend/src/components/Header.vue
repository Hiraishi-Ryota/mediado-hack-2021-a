<template>
  <v-app-bar
    app
    :color="color"
    dark
  >
    <v-app-bar-title>
      サービス名(仮)
    </v-app-bar-title>
  </v-app-bar>
</template>

<script>
export default {
  name: 'Header',
  props: {
    color: {
      type: String,
      default: ''
    }
  }
}
</script>