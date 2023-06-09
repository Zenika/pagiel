<script setup>
import Form from "../components/Form.vue";
</script>

<template>
  <section>
    <h1>Pagiel</h1>
    <h2>Mesurer l'impact environnemental de vos pages web</h2>
    <Form />
  </section>
</template>

<style lang="scss">
section {
  @include section-app;
}
h1 {
  @include h1;
}
h2 {
  @include h2;
}
</style>
