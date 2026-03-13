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
    <a
      @click="navigateTo('start')"
      :class="selected('start')"
      title="Start pagina met algemene statistieken"
    >Start</a>
    <a
      @click="navigateTo('gemeente')"
      :class="selected('gemeente')"
      title="Pagina met toegankelijkheidsgegevens per Gemeente"
    >Gemeente</a>
    <a
      @click="navigateTo('kaart')"
      :class="selected('kaart')"
      title="Pagina met toegankelijkheidsgegevens per gemeente op een kaart"
    >Kaart</a>
    <a
      @click="navigateTo('tg')"
      :class="selected('tg')"
      title="Pagina met een toegankelijkheid in alle gemeenten"
    >TG</a>
    <a
      @click="navigateTo('eml')"
      :class="selected('eml')"
      title="Pagina met locatiegegevens van WaarIsMijnStemlokaal vergeleken met verkiezingsuitslagen gegevens"
    >EML</a>
    <a
      @click="navigateTo('voortgang')"
      :class="selected('voortgang')"
      class="icon"
      title="Pagina met voortgang van aangeleverde gegevens door gemeenten voor aankomende verkiezing"
    >&#128203;</a>
    <input class="theme"
      type="checkbox"
      id="theme"
      :title="`Klik om pagina in ${thema ? 'licht' : 'donker'} thema te tonen.`"
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
  margin-left: 10px;
  -webkit-appearance: none;
  appearance: none;
  font-size: 1.3em;
  cursor: pointer;
  padding: 0px 3px;
}
.nav .theme:before {
  content: '\263C';
}
.nav .theme:checked:before {
  content: '\263D';
}
.nav .theme:hover {
  background-color: var(--color-button-hover);
  border-radius: 3px;
}

.nav a {
  text-decoration: none;
  color: var(--color-button-tekst);
  text-align: center;
  margin-left: 5px;
  padding: 5px 5px;
}

@media (min-width: 1200px) {
  .nav a {
    min-width: 80px;
  }
}

.nav a:hover {
  background-color: var(--color-button-hover);
  border-radius: 3px;
  text-decoration: underline;
  cursor: pointer;
}

.nav a.selected {
  font-weight: bold;
  text-decoration: underline;
}

.nav a:link,
.nav a:visited {
  text-decoration: none;
}

.nav .icon {
  font-size: 1.3em;
  padding-top: 0;
  text-decoration: none !important;
  color: var(--color-button-geselecteerd);
}

@media (max-width: 1280px) {
  .nav {
    position: unset;
    text-align: center;
  }
}

</style>
