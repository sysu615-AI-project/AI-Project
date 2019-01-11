<template>
    <img :src="require(`@/assets/chesses/${this.name}.png`)" :style="chessStyle" draggable="false"/>
</template>
<script>
export default {
  data() {
    return {
      name: "",
      id: "",
      ref: ""
    }
  },
  computed() {

  }
}
</script>