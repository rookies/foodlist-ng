<script setup lang="ts">
import { ref, onMounted } from "vue";
import API from "../api/main.ts";

const items = ref(null);
const item_refs = ref([]);

function load_items() {
  return API.list_items().then((data) => (items.value = data));
}

function delete_item(id: number) {
  if (confirm("Really delete the item?")) {
    return API.delete_item(id).then(load_items);
  }
}

function set_quantity(id: number, quantity: number) {
  /* TODO: Check for deletion! */
  return API.update_item(id, { quantity: quantity })
    .then(load_items)
    .then(function () {
      for (const item of item_refs.value) {
        if (item.dataset.id == id) {
          item.scrollIntoView({ behavior: "smooth" });
          break;
        }
      }
    });
}

onMounted(load_items);
</script>

<template>
  <div v-if="items === null">Loading...</div>

  <div v-else-if="items.length == 0">
    Click <em>Add</em>, to add categories or food.
  </div>

  <div v-else class="list-group">
    <div v-for="item in items" :key="item.id" :data-id="item.id" ref="item_refs" class="list-group-item">
      {{ item.quantity }}&times; {{ item.name }}
      <div class="dropdown">
        <button
          class="btn btn-secondary dropdown-toggle"
          type="button"
          data-toggle="dropdown"
        >
          Actions
        </button>
        <div class="dropdown-menu">
          <div class="dropdown-item btn-group" role="group">
            <button
              type="button"
              class="btn btn-sm btn-outline-danger"
              :disabled="item.quantity === 0"
              @click="set_quantity(item.id, 0)"
            >
              0
            </button>
            <button
              type="button"
              class="btn btn-sm btn-outline-danger"
              v-for="n in 3"
              :disabled="item.quantity < n"
              :key="n"
              @click="set_quantity(item.id, item.quantity - n)"
            >
              -{{ n }}
            </button>
          </div>
          <div class="dropdown-item btn-group" role="group">
            <button
              type="button"
              class="btn btn-sm btn-outline-success"
              v-for="n in 4"
              :key="n"
              @click="set_quantity(item.id, item.quantity + n)"
            >
              +{{ n }}
            </button>
          </div>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#">Add to shopping</a>
          <a class="dropdown-item" href="#">Hide from shopping</a>
          <a class="dropdown-item" href="#">Edit</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#" @click="delete_item(item.id)">Delete</a>
        </div>
      </div>
    </div>
  </div>
</template>
