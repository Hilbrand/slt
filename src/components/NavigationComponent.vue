<script setup lang="ts">
import { useRouter } from "vue-router";
import { jsonToNavigatie } from "@/ts/navigatie";
import type { InformatieType, PaginaID } from "@/ts/types";
import { onMounted, ref } from "vue";

const router = useRouter();

const props = defineProps<{
  informatie: InformatieType;
}>();

const thema = ref(false);

function navigateTo(page: PaginaID) {
  const copy = props.informatie;
  copy.pagina = page;
  router.push({ query: jsonToNavigatie(copy) });
}

function selected(page: PaginaID) {
  return props.informatie.pagina == page ? "selected" : "";
}

function bewaarThema() {
  localStorage.setItem("thema", JSON.stringify(thema.value));
}

onMounted(() => {
  const localStorageThema = localStorage.getItem("thema");

  if (localStorageThema === null) {
    thema.value = window?.matchMedia('(prefers-color-scheme: dark)').matches;
    bewaarThema();
  } else {
    thema.value = JSON.parse(localStorageThema);
  }
})
</script>

<template>
  <nav class="nav">
    <button
      @click="navigateTo('start')"
      :class="selected('start')"
      title="Start pagina met algemene statistieken"
    >Start</button>
    <button
      @click="navigateTo('gemeente')"
      :class="selected('gemeente')"
      title="Pagina met toegankelijkheidsgegevens per Gemeente"
    >Gemeente</button>
    <button
      @click="navigateTo('kaart')"
      :class="selected('kaart')"
      title="Pagina met toegankelijkheidsgegevens per gemeente op een kaart"
    >Kaart</button>
    <button
      @click="navigateTo('tg')"
      :class="selected('tg')"
      title="Specifieke toegankelijkheid in alle gemeenten"
    >TG</button>
    <button
      @click="navigateTo('eml')"
      :class="selected('eml')"
      title="Locatiegegevens van WaarIsMijnStemlokaal vergeleken met verkiezingsuitslagen gegevens"
    >EML Data</button>
    <button
      @click="navigateTo('voortgang')"
      :class="selected('voortgang')"
      title="Voortgang van aangeleverde gegevens door gemeenten voor aankomende verkiezing"
    >&#128203;</button>
    <input class="theme"
      type="checkbox"
      id="theme"
      title="Schakel tussen licht en donker thema"
      v-model="thema"
      @change="bewaarThema"/>
  </nav>
</template>

<style scoped>
.nav {
  position: absolute;
  right: 5px;
  top: 0px;
}
.nav .theme {
  padding-left: 10px;
  width: 30px;
  -webkit-appearance: none;
  appearance: none;
  font-size: 1.3em;
}
.nav .theme:before {
  content: '\263C';
}
.nav .theme:checked:before {
  content: '\263D';
}

.nav button {
  color: var(--color-button-tekst);
  vertical-align: middle;
  text-align: center;
  border: 1px solid var(--color-button-border);
  background-color: var(--color-button);
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
  background-color: var(--color-button-hover);
  cursor: pointer;
}

.nav button.selected {
  font-weight: bold;
  background: var(--color-button-geselecteerd);
}

@media (max-width: 1280px) {
  .nav {
    position: unset;
    text-align: center;
  }
}
</style>
