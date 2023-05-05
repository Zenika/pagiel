<script setup>
import Chip from "./Chip.vue";
const props = defineProps(["pages"]);
</script>

<template>
  <ul>
    <Chip
      v-for="(page, index) in props.pages"
      :text="page.name"
      :key="index"
      @handleDelete="pages.splice(index, 1)"
    ></Chip>
  </ul>
</template>

<style>
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}
</style>
