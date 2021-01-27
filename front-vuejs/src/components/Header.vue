<template>
  <div>
    <h1>Header</h1>
    <router-link to="/"
      ><img alt="Vue logo" src="./../assets/logo.png"
    /></router-link>
  </div>
</template>

<script>
export default {
  name: "Header",
  props: {
    msg: String
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
