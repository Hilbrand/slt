<script setup lang="ts">
import { useRouter } from "vue-router";
import { jsonToNavigatie } from "@/ts/navigatie";
import type { InformatieType, PaginaID } from "@/ts/types";

const router = useRouter();

const props = defineProps<{
  informatie: InformatieType;
}>();

function navigateTo(page: PaginaID) {
  const copy = props.informatie;
  copy.pagina = page;
  router.replace({ query: jsonToNavigatie(copy) });
}

function selected(page: PaginaID) {
  return props.informatie.pagina == page ? "selected" : "";
}
</script>

<template>
  <nav class="nav">
    <button @click="navigateTo('start')" :class="selected('start')">Start</button>
    <button @click="navigateTo('gemeente')" :class="selected('gemeente')">Gemeente</button>
    <button @click="navigateTo('kaart')" :class="selected('kaart')">Kaart</button>
    <button @click="navigateTo('eml')" :class="selected('eml')">EML Data</button>
  </nav>
</template>

<style scoped>
.nav {
  position: absolute;
  right: 5px;
  top: 0px;
}

.nav button {
  color: var(--text-color);
  vertical-align: middle;
  text-align: center;
  border: 1px solid #333;
  border-top: 0;
  border-radius: 0 0 5px 5px;
  padding: 10px;
  margin-left: 5px;
}

@media (min-width: 1600px) {
  .nav button {
    width: 100px;
  }
}

.nav a:link,
.nav a:visited {
  text-decoration: none;
}

.nav button:hover {
  background-color: #ccc;
  cursor: pointer;
}

.nav button.selected {
  font-weight: bold;
  background: #bbb;
}

@media (max-width: 1280px) {
  .nav {
    position: unset;
    text-align: center;
  }
}
</style>
