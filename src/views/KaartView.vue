<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import { createGemeenteStyleFunction, isAbove } from "@/ts/gemeenteStyle";
import {
  Kaart,
  maakGeoJsonKaartlaag,
  updateKaartlaag,
  type GeoLayer,
} from "@/ts/kaartlagen";
import { jsonToNavigatie } from "@/ts/navigatie";
import {
  TOEGANKELIJKHEDEN,
  TOEGANKELIJKHEDEN_IDS,
  type GemeenteDataType,
  type InformatieType,
  type LegendaTextType,
  type ToegankelijkhedenID,
  type ToegankelijkheidDataTypeKey,
} from "@/ts/types";
import Legenda from "@/components/LegendaComponent.vue";

const router = useRouter();

const props = defineProps<{
  informatie: InformatieType;
}>();

const toegankelijkhedenStore = useToegankelijkhedenStore();
const allData = ref<GemeenteDataType>({});

const toegankelijkheid = ref<ToegankelijkhedenID>("lb");
const toegankelijkheidText = computed<string>(() =>
  props.informatie?.toegankelijkheid && TOEGANKELIJKHEDEN[props.informatie?.toegankelijkheid] || "",
);
const percentage = ref(1);
const gemeente = ref("");

const laatsteToegankelijkheid = ref<ToegankelijkhedenID>();
const laatstePercentage = ref<number>(0);
const totalAbove = ref<number>(0);

const grootScherm = window.innerHeight > 800;

let kaartlaag = undefined as GeoLayer | undefined;
const featureGemeente = ref<string>("");

watch(
  () => toegankelijkhedenStore.loadedVerkiezing(),
  (newValue, oldValue) => {
    if (newValue !== "" && newValue !== oldValue) {
      allData.value = toegankelijkhedenStore.getGemeenteData();
      updateKaartlaag(kaartlaag, true);
    }
  },
  { immediate: true },
);

watch(
  () => props.informatie,
  () => {
    toegankelijkheid.value = props.informatie?.toegankelijkheid || "";
    percentage.value = props.informatie?.percentage || 1;
    gemeente.value = props.informatie?.gemeente || "";
    if (
      laatsteToegankelijkheid.value !== toegankelijkheid.value ||
      laatstePercentage.value !== percentage.value
      // laatsteVerkiezing.value !== verkiezing
    ) {
      laatsteToegankelijkheid.value = toegankelijkheid.value;
      laatstePercentage.value = percentage.value;
      totalAbove.value = calcTotal();
      updateKaartlaag(kaartlaag, true);
    }
  },
  { immediate: true, deep: true },
);

function calcTotal() {
  let sum = 0;

  for (const gem in allData.value) {
    const { above } = isAbove(allData.value, gem, toegankelijkheid.value, percentage.value);

    if (above) {
      sum += 1;
    }
  }
  return sum;
}

const kaart = ref<Kaart>();

function addLayer() {
  if (!toegankelijkheid.value) {
    return;
  }
  const tgStyle = createGemeenteStyleFunction(allData, toegankelijkheid, percentage);
  kaartlaag = maakGeoJsonKaartlaag("gemeenten.geojson", tgStyle);
  if (kaart.value) {
    kaart.value.addLayer(kaartlaag);
  }
  totalAbove.value = calcTotal();
  updateKaartlaag(kaartlaag, true);
}

// Als geen data beschikbaar, de kaartlaag zal worden toegevoegd als deze beschikbaar ingeladen is.
watch(
  () => toegankelijkhedenStore.loadedVerkiezing(),
  (newState) => {
    if (newState && !kaartlaag) {
      addLayer();
    }
  },
  { immediate: true, deep: true },
);

onMounted(() => {
  kaart.value = new Kaart(grootScherm, []);
  if (toegankelijkhedenStore.isDataForVerkiezing(props.informatie.verkiezing)) {
    // Als de data beschikbaar is voeg de kaartlaag toe.
    addLayer();
  }
  kaart.value.addFeatureListener((feature) => {
    featureGemeente.value = feature.get("c");
  });
});


function wisselToegankelijkheid(event: Event) {
  const e = event.target as HTMLInputElement;
  const copy = props.informatie;
  copy.toegankelijkheid = e.value as ToegankelijkhedenID;
  router.push({ query: jsonToNavigatie(copy) });
}

function selected(tg: string): boolean {
  return props.informatie?.toegankelijkheid === tg;
}

function handleSlider() {
  const copy = props.informatie;
  copy.percentage = percentage.value;
  router.push({ query: jsonToNavigatie(copy) });
}

function featureGemeenteName(): string {
  if (featureGemeente.value) {
    return toegankelijkhedenStore.getGemeenteName(featureGemeente.value);
  }
  return featureGemeente.value;
}
function heeft(state: ToegankelijkheidDataTypeKey): boolean {
  return (toegankelijkheid.value === 'gt' && (state == 'l' || state == 'a'))
      || (toegankelijkheid.value === 'to' && (state == 't' || state == 'g'));
}

function gegevensBeschikbaar(): boolean {
  const data = allData.value;

  return featureGemeente.value
      && data
      && data[featureGemeente.value]
      && data[featureGemeente.value][2]
      && data[featureGemeente.value][2][toegankelijkheid.value] && true || false;
}

function aanwezig(state: ToegankelijkheidDataTypeKey): number {
  if (gegevensBeschikbaar()) {
    return allData.value[featureGemeente.value][2][toegankelijkheid.value][state] || 0;
  }
  return 0;
}

function totalGem(): number {
  if (gegevensBeschikbaar()) {
    return allData.value[featureGemeente.value][1] || 0;
  }
  return 0;
}
const legendaText = {
  ja: "Gemeente waar de toegankelijkheid in minimaal het percentage stemlokalen aanwezig is",
  nee: "Gemeenten waar in geen enkel stemlokaal de toegankelijkheid aanwezig is",
  onbekend:
    "Gemeenten waar de toegankelijkheid in minder stemlokalen dan het percentage aanwezig is, of deze informatie onbekend is",
  geenGegevens: "Geen gegevens",
  titel: true,
} as LegendaTextType;
</script>

<template>
  <div class="mapContent">
    <select class="select" @change="wisselToegankelijkheid">
    <option v-for="row in TOEGANKELIJKHEDEN_IDS" :key="row"
        :value="row"
        :selected="selected(row)">
      {{ TOEGANKELIJKHEDEN[row] }}
    </option>
    </select>
    <div class="mapSelector">
      <h3>Percentage</h3>
      <p>
        In {{ totalAbove }} gemeenten is {{ percentage }}% van de stemlokalen
        {{ toegankelijkheidText }}.
      </p>
      <div class="slider-container">
        <input
          type="range"
          min="1"
          max="100"
          v-model="percentage"
          class="slider"
          @change="handleSlider" />
      </div>
    </div>
    <div id="map">
      <div id="hover">
        <h4 class="hover-title">{{ featureGemeenteName() }}</h4>
        <template v-if="totalGem() > 0">
          <p>Aantal stemlokaties waar {{ toegankelijkheidText }}:</p>
          <div class="hover-table">
            <template v-if="heeft('l')">
              <div>Lokaal</div>
              <div>{{ aanwezig("l") }}</div>
            </template>
            <template v-if="heeft('a')">
              <div>Op afstand</div>
              <div>{{ aanwezig("a") }}</div>
            </template>
            <template v-if="heeft('t')">
              <div>Toegankelijk</div>
              <div>{{ aanwezig("t") }}</div>
            </template>
            <template v-if="heeft('g')">
              <div>Genderneutraal</div>
              <div>{{ aanwezig("g") }}</div>
            </template>
            <template v-if="toegankelijkheid != 'gt'">
              <div>Aanwezig</div>
              <div>{{ aanwezig("j") }}</div>
            </template>
            <div>Nee</div>
            <div>{{ aanwezig("n") }}</div>
            <div>Onbekend</div>
            <div>{{ aanwezig("") }}</div>
            <div class="hover-table-last">Totaal</div>
            <div class="hover-table-last">{{ totalGem() }}</div>
          </div>
        </template>
        <div v-else>Voor deze gemeente zijn nog geen gegevens beschikbaar.</div>
      </div>
      <div class="kaart-hint" v-if="!grootScherm">Gebruik 2 vingers om de kaart te verplaatsen.</div>
    </div>
    <Legenda :legendaText="legendaText" />
  </div>
</template>

<style scoped>
.selecties {
  display: grid;
  grid-template-columns: 15px 1fr;
  align-items: center;
  column-gap: 7px;
}

.slider-container {
  margin-right: 10px;
}

.slider {
  width: 100%;
}

.mapContent {
  display: grid;
  grid-template-columns: 20em 1fr;
}

.mapSelector {
  margin-top: 10px;
  margin-left: 10px;
  border-right: 1px solid var(--color-map-selectie-border);
}

#map {
  position: relative;
  height: calc(100dvh - 72px);
  margin: 0;
  padding: 0;
}

#hover {
  position: absolute;
  display: inline-block;
  height: 220px;
  width: 200px;
  z-index: 100;
  background-color: var(--color-popup);
  color: var(--color-popup-tekst);
  text-align: left;
  border-radius: 6px;
  border-color: var(--color-popup-border);
  border-width: 3px;
  border-style: solid;
  padding: 5px;
  transform: translateX(3%);
  visibility: hidden;
  pointer-events: none;
}

#hover h4 {
  margin: 0;
  padding: 0;
}

.hover-title {
  text-align: center;
}

.hover-table {
  display: grid;
  grid-template-columns: auto auto;
}

.hover-table-last {
  border-top: 1px solid var(--color-popup-border);
}

@media (max-width: 1024px) {
  .mapContent {
    display: block;
    grid-template-columns: 20em 1fr;
  }
  #map {
    margin: 0 20px;
  }
  .grid td:first-child {
    width: 50%;
  }
  .row {
    margin-bottom: 1rem;
  }
}
.kaart-hint {
  margin-bottom: 10px;
}
</style>
