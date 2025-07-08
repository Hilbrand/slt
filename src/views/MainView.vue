<script setup lang="ts">
import Navigation from "@/components/NavigationComponent.vue";
import { useEmlMismatchesStore } from "@/stores/emlMismatchesStore";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import { jsonToNavigatie, navigatieToJson } from "@/ts/navigatie";
import { VERKIEZING_IDS, VERKIEZINGEN, type InformatieType, type VerkiezingID } from "@/ts/types";
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import Eml from "./EmlView.vue";
import Gemeente from "./GemeenteView.vue";
import Kaart from "./KaartView.vue";
import Start from "./StartView.vue";

const route = useRoute();
const router = useRouter();

const informatie = ref<InformatieType>({} as InformatieType);

const toegankelijkhedenStore = useToegankelijkhedenStore();
const emlMismatchesStore = useEmlMismatchesStore();

watch(
  () => route.query,
  (newValue) => {
    informatie.value = navigatieToJson(newValue);
  },
  { immediate: true, deep: true },
);

watch(
  () => informatie,
  (newValue) => {
    router.replace({ query: jsonToNavigatie(newValue.value) });
    update(informatie.value);
  },
  { immediate: true, deep: true },
);

const title = computed<string>(() => {
  switch (informatie.value?.pagina) {
    case "eml":
      return "EML Data"
    case "start":
      return "";
    case "kaart":
      return "op de kaart";
    case "gemeente":
      return toegankelijkhedenStore.getGemeenteName(informatie.value?.gemeente);
    default:
      return "";
  }
});

function wisselVerkiezing(event: Event) {
  const e = event.target as HTMLInputElement;
  const copy = informatie.value;
  copy.verkiezing = e.value as VerkiezingID;
  router.replace({ query: jsonToNavigatie(copy) });
}

async function update(informatie: InformatieType) {
  if (
    informatie &&
    informatie?.verkiezing &&
    !toegankelijkhedenStore.isDataForVerkiezing(informatie.verkiezing)
  ) {
    await toegankelijkhedenStore.loadData(informatie.verkiezing);
    await emlMismatchesStore.loadData(informatie.verkiezing);
  }
}
</script>

<template>
  <header class="header">
    <select class="verkiezingen" @change="wisselVerkiezing">
      <option v-for="verkiezing in VERKIEZING_IDS"
        :key="verkiezing"
        :value="verkiezing"
        :selected="informatie.verkiezing === verkiezing">
        {{ VERKIEZINGEN[verkiezing] }}
      </option>
    </select>
    <Navigation class="nav" :informatie="informatie" />
    <h1>Stemlokaaltoegankelijkheid {{ title }}</h1>
    <h2>{{ VERKIEZINGEN[informatie.verkiezing] }}</h2>
  </header>
  <main class="main">
    <Kaart v-if="informatie.pagina == 'kaart'" :informatie="informatie" />
    <Gemeente v-else-if="informatie.pagina == 'gemeente'" :informatie="informatie" />
    <Eml v-else-if="informatie.pagina == 'eml'" :informatie="informatie" />
    <Start v-else :informatie="informatie" />
  </main>
  <footer class="footer">
    <p>
      De informatie op deze pagina is gebaseerd met de gegevens die beschikaar zijn op de website
      <a href="https://www.waarismijnstemlokaal.nl" target="_blank"
        >https://www.waarismijnstemlokaal.nl</a
      >. De gegevens zijn gebaseerd op het bestand met id:
      <code>{{ toegankelijkhedenStore.getResourceId() }}</code>.
      Meer informatie over dit project is te vinden op <a href="https://github.com/hilbrand/slt" target="_blank"
      >https://github.com/hilbrand/slt</a>.
    </p>
  </footer>
</template>

<style scoped>
.header {
  position: fixed;
  width: 100%;
  height: 130px;
  text-align: center;
  margin: 0;
  border-bottom: 1px solid #333;
  background-color: white;
  z-index: 10000;
}
.verkiezingen {
  position: absolute;
  left: 10px;
  top: 0px;
}
.footer {
  width: 100%;
}
.main {
  padding-top: 130px;
}

@media (max-width: 1280px) {
  .header {
    height: 160px;
  }
  .main {
    padding-top: 160px;
  }
}

@media (max-width: 1024px) {
  .header {
    height: 165px;
  }
  .header h1 {
    font-size: 1.2em;
  }
  .header h2 {
    font-size: 1em;
  }
  .header .verkiezingen {
    left: 5px;
    top: 140px;
  }
  .main {
    padding-top: 160px;
  }
  .footer p {
    margin: 10px;
  }
}
</style>
