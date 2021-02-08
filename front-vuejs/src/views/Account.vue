<template>
  <div>
    <h1>Account</h1>
    <div>{{ accountData.owner }}</div>
    <div>Balance: {{ accountData.balance }}</div>
    <h3>Dernières opérations</h3>
    <ul id="example-2">
      <li
        v-for="(operation, index) in accountData.lastoperations"
        v-bind:key="index"
      >
        {{ index }} - {{ operation.date }} - {{ operation.type }} -
        {{ operation.value }} - {{ operation.description }}
      </li>
    </ul>
  </div>
</template>
<script>
export default {
  name: "Account",
  props: {
    accountNumber: String
  },
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL ?? "http://localhost:3031",
      accountData: []
    };
  },
  created() {
    document.title = "Mon compte";
    console.log("fetch: " + this.apiUrl + "/?account=001");
    fetch("http://localhost:3040/?account=001")
      .then(response => response.json())
      .then(data => (this.accountData = data))
      .catch(error => console.log(error));
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
