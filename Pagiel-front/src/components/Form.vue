<script setup>
import { ref } from "vue";
import ChipList from "./ChipList.vue";

const pages = ref([
  { name: "Page 1", url: "https://www.google.com" },
  { name: "Page 2", url: "https://www.google.com" },
]);
const pageName = ref("");
const url = ref("");

const analyzePages = () => {
  console.log(
    "TODO : créer le fichier urls.yaml ici et appeler ensuite le pagiel.sh"
  );
};

const pageAlreadyExists = (newPage) => {
  return pages.value.some((page) => page.name === newPage.name);
};

const addAnotherPage = () => {
  const newPage = { name: pageName.value, url: url.value };
  if (
    !pageAlreadyExists(newPage) &&
    pageName.value !== "" &&
    url.value !== ""
  ) {
    pages.value.push(newPage);
    url.value = "";
    pageName.value = "";
  }
};
</script>

<template>
  <form>
    <input v-model="url" type="text" placeholder="URL" />
    <input v-model="pageName" type="text" placeholder="Nom de la page" />
    <button type="button" @click="addAnotherPage">
      Mesurer une autre page
    </button>
    <ChipList v-if="pages.length > 0" :pages="pages" />

    <button type="submit" @click="analyzePages">Analyser</button>
  </form>
</template>
