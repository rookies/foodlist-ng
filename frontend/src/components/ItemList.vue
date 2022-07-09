<script setup lang="ts">
import { ref, onMounted } from "vue";
import API from "../api/main.ts";

const presets = {
  consuming: {
    params: {
      order_by: "quantity",
      order_direction: "desc",
      custom_filter: "",
    },
    style: {
      strikethrough_empty: true,
      show_tags: true,
      colors: {
        empty: "dark",
        expired: "danger",
        soon_expired: "warning",
      },
    },
  },
  shopping: {
    params: {
      order_by: "id",
      order_direction: "asc",
      custom_filter: "shopping",
    },
    style: {
      strikethrough_empty: false,
      show_tags: false,
      colors: {
        empty: "",
        expired: "",
        soon_expired: "",
      },
    },
  },
};

const current_preset = ref("consuming");
const item_groups = ref(null);
const item_refs = ref([]);

function get_preset() {
  return presets[current_preset.value];
}

function get_item_color_class(item: object) {
  if (item.quantity == 0) {
    return "list-group-item-" + get_preset().style.colors.empty;
  }
  if (item.expired) {
    return "list-group-item-" + get_preset().style.colors.expired;
  }
  if (item.soon_expired) {
    return "list-group-item-" + get_preset().style.colors.soon_expired;
  }
  return "";
}

function group_items(items: object[], tag_category: string) {
  const groups = new Map();
  for (const item of items) {
    let group = "";
    if (tag_category) {
      for (const tag of item.tags) {
        if (tag.startsWith(tag_category + ":")) {
          group = tag.slice(tag_category.length + 1);
          break;
        }
      }
    }

    if (!groups.has(group)) {
      groups.set(group, {
        title: group,
        items: [],
      });
    }

    groups.get(group).items.push(item);
  }

  return groups;
}

function scroll_to_item(id: number) {
  for (const item of item_refs.value) {
    if (item.dataset.id == id) {
      item.scrollIntoView({ behavior: "smooth" });
      break;
    }
  }
}

function load_items() {
  return API.list_items(get_preset().params).then((data) => {
    /* TODO: Pass tag_category */
    item_groups.value = group_items(data, "loc");
  });
}

function delete_item(id: number) {
  if (confirm("Really delete the item?")) {
    return API.delete_item(id).then(load_items);
  }
}

function update_item(id: number, values: object) {
  return API.update_item(id, values)
    .then(load_items)
    .then(() => scroll_to_item(id));
}

function set_quantity(id: number, quantity: number) {
  /* TODO: Check for deletion! */
  return update_item(id, { quantity: quantity });
}

function create_tag(item_id: number, tag: string) {
  return API.create_tag(item_id, tag)
    .then(load_items);
  /*  .then(() => scroll_to_item(item_id));*/
  /* TODO: Add option to disable scrolling */
}

function delete_tag(item_id: number, tag: string) {
  return API.delete_tag(item_id, tag)
    .then(load_items)
    .then(() => scroll_to_item(item_id));
}

function create_tag_submit(item_id: number, ev: event) {
  create_tag(item_id, ev.target.elements[0].value);
  ev.target.elements[0].value = "";
}

onMounted(load_items);
</script>

<template>
  <div v-if="item_groups === null">Loading...</div>

  <div v-else-if="item_groups.length == 0">
    Click <em>Add</em>, to add categories or food.
  </div>

  <div v-else v-for="[key, group] in item_groups" :key="key">
    <h5 v-if="group.title">{{ group.title }}</h5>
    <div class="list-group">
      <div
        v-for="item in group.items"
        :key="item.id"
        :data-id="item.id"
        ref="item_refs"
        class="list-group-item"
        :class="get_item_color_class(item)"
      >
        <div class="float-left">
          <s
            v-if="get_preset().style.strikethrough_empty && item.quantity == 0"
          >
            {{ item.name }}
          </s>
          <span v-else>{{ item.name }}</span>
          <br />
          <small class="text-muted">
            {{ item.quantity }} / {{ item.min_quantity }}
            <span v-if="item.temporary_additional_min_quantity">
              + {{ item.temporary_additional_min_quantity }}
            </span>
            <span v-if="item.best_before && item.quantity">
              &ndash; {{ item.best_before }}
            </span>
          </small>
          <span v-if="get_preset().style.show_tags">
            <br />
            <span v-for="tag in item.tags" :key="tag" class="badge badge-secondary">
              {{ tag }}
              <a href="#" @click.prevent="delete_tag(item.id, tag)">&times;</a>
            </span>
            <form @submit.prevent="create_tag_submit(item.id, $event)">
              <input type="text" class="form-control form-control-sm" />
            </form>
          </span>
        </div>
        <div class="float-right">
          <div class="dropleft">
            <button
              class="btn btn-secondary dropdown-toggle"
              type="button"
              data-toggle="dropdown"
            ></button>
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
              <button
                class="dropdown-item"
                @click="update_item(item.id, { temporary_additional_min_quantity: item.temporary_additional_min_quantity + 1 })"
              >
                Add to shopping
              </button>
              <button
                class="dropdown-item"
                v-if="item.temporary_additional_min_quantity > 0"
                @click="update_item(item.id, { temporary_additional_min_quantity: 0 })"
              >
                Remove from shopping ({{ item.temporary_additional_min_quantity }})
              </button>
              <button
                class="dropdown-item"
                v-if="!item.hidden_on_shopping"
                @click="update_item(item.id, { hidden_on_shopping: true })"
              >
                Hide from shopping
              </button>
              <button
                class="dropdown-item"
                v-if="item.hidden_on_shopping"
                @click="update_item(item.id, { hidden_on_shopping: false })"
              >
                Unhide from shopping
              </button>
              <button class="dropdown-item">Edit</button>
              <div class="dropdown-divider"></div>
              <button
                class="dropdown-item"
                @click="delete_item(item.id)"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
