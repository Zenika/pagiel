<template>
  <div>
    <h1>Account</h1>
    <button v-on:click="getAccountData">Get account Data</button>
    <div>{{ accountData }}</div>
    <div>Balance: {{ accountData.balanace }}</div>
  </div>
</template>
<script>
export default {
  name: "Account",
  props: {
    msg: String
  },
  data() {
    return {
      accountData: []
    };
  },
  created() {
    fetch("http://localhost:3031/?account=001")
      .then(response => response.json())
      .then(data => console.log(data))
      .then(data => (this.accountData = data))
      .catch(error => console.log(error));
  },
  methods: {
    getAccountData() {
      fetch("http://localhost:3031/?account=001")
        // With the fetch API we need to call the json() function which reads the response to the completion.
        // This also returns a promise, so we need to chain a new then method to get the JSON data that we want.
        .then(response => response.json())
        .then(data => (this.accountData = data));
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
