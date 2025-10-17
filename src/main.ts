import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { useGemeentenStore } from "@/stores/gemeentenStore";

import App from "./App.vue";
import MainView from "./views/MainView.vue";

const routes = [{ path: "", component: MainView }];

const router = createRouter({
  history: createWebHistory("/slt"),
  routes,
});

const app = createApp(App);

app.use(createPinia());
app.use(router);

const gemeentenStore = useGemeentenStore();

gemeentenStore.loadData().then(() => {
  app.mount("#app");
});
