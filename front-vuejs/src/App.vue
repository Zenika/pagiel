<template>
  <div id="app">
    <Header />
    <div id="nav">
      <router-link to="#">Nos métiers</router-link> |
      <a href="#">Nous connaître</a> |
      <router-link to="#">Développement responsable</router-link> |
      <router-link to="/login">Login</router-link>
    </div>
    <router-view />
    <Footer />
  </div>
</template>

<script>
import Footer from "./components/Footer.vue";
import Header from "@/components/Header";

export default {
  name: "App",
  components: {
    Header,
    Footer
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
