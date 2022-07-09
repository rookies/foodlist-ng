import { createApp } from "vue";
import { createRouter, createWebHashHistory } from "vue-router";

import App from "./App.vue";
import ItemList from "./components/ItemList.vue";

const routes = [
  {
    path: "/",
    redirect: "/list/consuming",
  },
  {
    path: "/list/:preset",
    component: ItemList,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes: routes,
});

const app = createApp(App);
app.use(router);
app.mount("#app");
