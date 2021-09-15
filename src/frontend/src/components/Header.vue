<template>
  <v-app-bar
    app
    :color="color"
    dark
  >
    <v-app-bar-title>
      <div style="width: 400px">
        {{ appName }}
      </div>
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
  },
  data() {
    return {
      appName: "サービス名（仮）"
    }
  },
  mounted: function() {
    this.appName = this.color === 'orange'
      ? '章分活'
      : '眼力(シリョク)アゲたい⤴⤴⤴書店' 
  },
}
</script>