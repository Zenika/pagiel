<template>
  <div>
    <h1>Login</h1>
    <div class="button-block">
      <router-link to="/account">
        <button>Connexion</button>
      </router-link>
    </div>
  </div>
</template>
<script>
export default {
  name: "Login",
  props: {
    msg: String
  },
  created() {
    document.title = "Login";
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
