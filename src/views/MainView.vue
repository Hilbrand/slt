<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useEmlMismatchesStore } from "@/stores/emlMismatchesStore";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import { jsonToNavigatie, navigatieToJson } from "@/ts/navigatie";
import { VERKIEZING_IDS, VERKIEZINGEN, Visualisatie, type InformatieType, type VerkiezingID } from "@/ts/types";
import Navigation from "@/components/NavigationComponent.vue";
import Eml from "./EmlView.vue";
import Gemeente from "./GemeenteView.vue";
import Kaart from "./KaartView.vue";
import Start from "./StartView.vue";
import Toegankelijkheden from "./ToegankelijkhedenView.vue";
import Voortgang from "./VoortgangView.vue";

const route = useRoute();
const router = useRouter();

const informatie = ref<InformatieType>({} as InformatieType);

const toegankelijkhedenStore = useToegankelijkhedenStore();
const emlMismatchesStore = useEmlMismatchesStore();
const visualisatie = ref(false);

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
    visualisatie.value = newValue.value.visualisatie == Visualisatie.GRAFIEK;
    update(informatie.value);
  },
  { immediate: true, deep: true },
);

const titel = computed<string>(() => {
  switch (informatie.value?.pagina) {
    case "eml":
      return "EML Data"
    case "start":
      return "";
    case "kaart":
      return "op de kaart";
    case "gemeente":
      return toegankelijkhedenStore.getGemeenteName(informatie.value?.gemeente);
    case "voortgang":
      return "aanlevervoortgang";
    case "tg":
      return "";
    default:
      return "";
  }
});

function wisselVerkiezing(event: Event) {
  const e = event.target as HTMLInputElement;
  const copy = informatie.value;
  copy.verkiezing = e.value as VerkiezingID;
  router.push({ query: jsonToNavigatie(copy) });
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
function veranderVisualisatie(event: Event) {
  const e = event.target as HTMLInputElement;
  const copy = informatie.value;
  copy.visualisatie = e.checked ?  Visualisatie.GRAFIEK : Visualisatie.TABEL;
  router.push({ query: jsonToNavigatie(copy) });
}
</script>

<template>
  <header class="header">
    <select class="verkiezingen" @change="wisselVerkiezing">
      <option v-for="verkiezing in VERKIEZING_IDS"
        :key="verkiezing"
        :value="verkiezing"
        :selected="informatie.verkiezing === verkiezing">
        {{ VERKIEZINGEN[verkiezing].naam }}
      </option>
    </select>
    <Navigation class="nav" :informatie="informatie" />
    <h1>Stemlokaaltoegankelijkheid <span class="titel">{{ titel }}</span></h1>
    <h2 class="verkiezing-naam">{{ VERKIEZINGEN[informatie.verkiezing].naam }}</h2>
    <input
      type="checkbox"
      titel="Toon gegevens als Grafiek of Tabel"
      class="vis"
      v-model="visualisatie"
      @change="veranderVisualisatie"/>
  </header>
  <main class="main">
    <Kaart v-if="informatie.pagina == 'kaart'" :informatie="informatie" />
    <Gemeente v-else-if="informatie.pagina == 'gemeente'" :informatie="informatie" />
    <Eml v-else-if="informatie.pagina == 'eml'" :informatie="informatie" />
    <Voortgang v-else-if="informatie.pagina == 'voortgang'" :informatie="informatie" />
    <Toegankelijkheden v-else-if="informatie.pagina == 'tg'" :informatie="informatie" />
    <Start v-else :informatie="informatie" />
  </main>
  <footer class="footer">
    <p>
      De informatie op deze pagina is gebaseerd met de gegevens die beschikaar zijn op de website
      <a href="https://www.waarismijnstemlokaal.nl" target="_blank"
        >https://www.waarismijnstemlokaal.nl</a
      >. De gegevens zijn gebaseerd op het bestand met id:
      <code>{{ toegankelijkhedenStore.getResourceId() }}</code>.
   </p>
    <p>'Niet verplichte toegankelijkheden' is de som van alle toegankelijkheden behalve de verplichte
      'Toegankelijk voor mensen met een lichamelijke beperking'.
   </p>
    <p>
      Meer informatie over dit project is te vinden op <a href="https://github.com/hilbrand/slt" target="_blank"
      >https://github.com/hilbrand/slt</a>.
    </p>
  </footer>
</template>

<style scoped>
.header {
  position: fixed;
  width: 100vw;
  height: 130px;
  text-align: center;
  margin: 0;
  border-bottom: 1px solid var(--color-header-bottom);
  background-color: var(--color-achtergrond);
  box-shadow: 0 1px 5px var(--color-header-bottom);
  z-index: 10000;
}

.vis {
  position: absolute;
  top: 90px;
  right: 0px;
  width: 30px;
  -webkit-appearance: none;
  appearance: none;
  font-size: 1.3em;
  cursor: pointer;
}
.vis:before {
  content: 'T';
}
.vis:checked:before {
  content: '\1F4CA';
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
  background-color: var(--color-main);
  position: relative;
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
    height: 105px;
  }
  .header h1 {
    font-size: 1.2em;
  }
  .header h2 {
    display: none;
    font-size: 1em;
  }
  .header .verkiezingen {
    left: 5px;
    top: 78px;
  }
  .vis {
    top:45px;
    right: 0px;
  }
  .main {
    padding-top: 105px;
  }
  .footer p {
    margin: 10px;
  }
}
@media (max-width: 600px) {
  .titel {
    display: none;
  }
}
</style>
