<script setup lang="ts">
import ItemList from "./components/ItemList.vue";
</script>

<template>
  <div class="container">
    <header>
      <div class="row">
        <div class="col-md-12">
          <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="/">Foodlist</a>
          </nav>
        </div>
      </div>
    </header>
    <main>
      <div class="row">
        <div class="col-md-12">
          <ItemList />
        </div>
      </div>
    </main>
  </div>
</template>
