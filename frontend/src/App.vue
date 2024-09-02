<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
 

    <div>
      <ul>
        <li><RouterLink to="/">Home</RouterLink></li>
        <li><RouterLink to="/list">list</RouterLink></li>
      </ul>
    </div>
  

  <RouterView />
</template>

<style scoped>
ul{
  margin: 0;
  padding: 0;
}
li{
  display: inline;
  margin: 10px;
}

</style>


