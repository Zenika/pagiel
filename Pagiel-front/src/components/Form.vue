<script setup>
import { computed, ref, watch } from "vue";
import ChipList from "./ChipList.vue";

const webPages = ref([]);
const pageName = ref("");
const url = ref("");
const submissionError = ref(false);

watch(pageName, () => {
  if (submissionError.value) {
    submissionError.value = false;
  }
});

const areBothInputsFilled = computed(() => {
  return pageName.value !== "" && url.value !== "";
});

const areBothInputsEmpty = computed(() => {
  return pageName.value === "" && url.value === "";
});

const isAnalysisPossible = computed(() => {
  if (areBothInputsFilled.value) return true;
  else if (areBothInputsEmpty.value) return webPages.value.length > 0;
  else return false;
});

const pageAlreadyExists = (newPage) => {
  return webPages.value.some((page) => page.name === newPage.name);
};

const addNewWebPage = () => {
  const newPage = { name: pageName.value, url: url.value };
  if (!pageAlreadyExists(newPage)) {
    webPages.value.push(newPage);
    url.value = "";
    pageName.value = "";
  } else {
    submissionError.value = true;
  }
};

const analyzeWebPages = () => {
  if (isAnalysisPossible) {
    if (areBothInputsFilled.value)
      webPages.value.push({ name: pageName.value, url: url.value });

    fetch("http://localhost:5000/process-url", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(webPages.value),
    }).catch((error) => {
      console.error(error);
    });
  }
};
</script>

<template>
  <form>
    <input v-model="url" type="text" placeholder="URL" autofocus />
    <span v-if="submissionError">Nom déjà existant</span>
    <input
      :class="{ error: submissionError }"
      v-model="pageName"
      type="text"
      placeholder="Nom de la page"
    />
    <button
      type="button"
      :disabled="!areBothInputsFilled"
      @click="addNewWebPage"
    >
      Ajouter une autre page
    </button>

    <button
      class="submit-button"
      type="submit"
      @click="analyzeWebPages"
      :disabled="!isAnalysisPossible"
    >
      Analyser
    </button>
    <ChipList v-if="webPages.length > 0" :webPages="webPages" />
  </form>
</template>

<style lang="scss" scoped>
button {
  @include button;
}
form {
  @include form;
}
input {
  @include input;
}

.error {
  border: 1px solid red;
}

span {
  font-style: italic;
  color: red;
}
.submit-button {
  @include button-green;
}
</style>
