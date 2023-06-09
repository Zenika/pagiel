<script setup>
import Chip from "./Chip.vue";
const props = defineProps(["webPages"]);
</script>

<template>
  <ul>
    <Chip
      v-for="(page, index) in webPages"
      :text="page.name"
      :key="index"
      @handleDelete="webPages.splice(index, 1)"
    ></Chip>
  </ul>
</template>

<style lang="scss" scoped>
ul {
  @include chipList;
}
</style>
