<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/color_hex.png" width="125" height="125" />
    <div class="wrapper">
      <HelloWorld msg="Palette Generator" />
    </div>
  </header>

  <main>
    <DataTable @table-data-fetched="handleTableData" />
  </main>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import DataTable from './components/DataTable.vue';

export default {
    components: { HelloWorld, DataTable },
    data() {
      return {
      };
    },
    methods: {
      handleTableData(data){
      }
    }
};
</script>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
    margin-top: 30px; /* Adjust the value as needed */
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
