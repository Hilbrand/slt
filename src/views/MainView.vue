<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useEmlMismatchesStore } from "@/stores/emlMismatchesStore";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import { jsonToNavigatie, navigatieToJson } from "@/ts/navigatie";
import { TOEGANKELIJKHEDEN, VERKIEZING_IDS, VERKIEZINGEN, Visualisatie, type InformatieType, type VerkiezingID } from "@/ts/types";
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
const visualisatie = ref(Visualisatie.GRAFIEK);

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
    visualisatie.value = newValue.value.visualisatie;
    update(informatie.value);
  },
  { immediate: true, deep: true },
);

const titel = computed<string>(() => {
  switch (informatie.value?.pagina) {
    case "eml":
      return "EML vs WaarIsMijnStemlokaal"
    case "start":
      return "Stemlokaaltoegankelijkheid";
    case "kaart":
      return "Op de kaart";
    case "gemeente":
      return toegankelijkhedenStore.getGemeenteName(informatie.value?.gemeente);
    case "voortgang":
      return "Aanlevervoortgang";
    case "tg":
      return TOEGANKELIJKHEDEN[informatie.value.toegankelijkheid];
    default:
      return "Stemlokaaltoegankelijkheid";
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
  copy.visualisatie = e.value as Visualisatie;
  router.push({ query: jsonToNavigatie(copy) });
}
function nietZelf() {
  return informatie.value?.pagina == 'gemeente'
      && toegankelijkhedenStore.isNietDeelnemendeGemeente(toegankelijkhedenStore.getGemeenteName(informatie.value?.gemeente)) ? '1': '';
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
    <h1 class="titel">{{ titel }} <sup>{{ nietZelf() }}</sup></h1>
    <h2 class="verkiezing-naam">{{ VERKIEZINGEN[informatie.verkiezing].naam }}</h2>
    <div v-if="['start', 'gemeente', 'tg'].includes(informatie?.pagina)" class="visu">
      <label>
        <input
          type="radio"
          v-model="visualisatie"
          :value="Visualisatie.GRAFIEK"
          @change="veranderVisualisatie"
        />Grafiek</label>
      <label>
        <input
          type="radio"
          v-model="visualisatie"
          :value="Visualisatie.TABEL"
          @change="veranderVisualisatie"
        />Tabel</label>
    </div>
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
      <a href="https://WaarIsMijnStemlokaal.nl" target="_blank"
        >https://WaarIsMijnStemlokaal.nl</a
      >. De gegevens zijn gebaseerd op het bestand met id:
      <code>{{ toegankelijkhedenStore.getResourceId() }}</code>.
    </p>
    <details>
      <summary>Uitleg Niet verplichte toegankelijkheden</summary>
      <p><b>Niet verplichte toegankelijkheden</b> is de som van alle toegankelijkheden behalve de verplichte
         'Toegankelijk voor mensen met een lichamelijke beperking'.
         In dit cijfer wordt de aanwezigheid van een toilet meegenomen en
         voor Gebarentolk wordt op locatie of op afstand meegenomen als aanwezig.
      </p>
    </details>
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

.visu {
  position: absolute;
  top: 105px;
  right: 10px;
}

.verkiezingen {
  position: absolute;
  left: 10px;
  top: 0px;
}
.footer {
  width: 100%;
}
.footer > * {
  margin: 10px;
}
.main {
  padding-top: 130px;
  background-color: var(--color-main);
  position: relative;
}

@media (max-width: 1280px) {
  .verkiezing-naam {
    display: none;
  }
}

@media (max-width: 1024px) {
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
}
</style>
