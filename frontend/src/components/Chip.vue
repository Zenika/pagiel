<script setup>
const props = defineProps({ text: String });
const emit = defineEmits(["handleDelete"]);
</script>

<template>
  <li class="chip">
    <p>{{ text }}</p>
    <span class="deleteBtn" @click="emit('handleDelete')">&times;</span>
  </li>
</template>

<style lang="scss" scoped>
.chip {
  @include chip;
}
</style>
