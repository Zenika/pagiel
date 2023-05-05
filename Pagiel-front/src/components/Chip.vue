<script setup>
const props = defineProps({ text: String });
const emit = defineEmits(["handleDelete"]);
</script>

<template>
  <li class="chip">
    <p>{{ props.text }}</p>
    <span class="deleteBtn" @click="emit('handleDelete')">&times;</span>
  </li>
</template>

<style>
.chip {
  display: inline-block;
  padding: 0 10px;
  height: 30px;
  font-size: 16px;
  line-height: 30px;
  border-radius: 25px;
  background-color: #f1f1f1;
  margin: 5px;
}

.chip p {
  float: left;
  margin: 0;
}

.chip .deleteBtn {
  padding-left: 15px;
  float: right;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

.chip .deleteBtn:hover {
  color: #000;
}
</style>
