<script setup lang="ts">
import Legenda from "@/components/LegendaComponent.vue";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import { createGemeenteStyleFunction, isAbove } from "@/ts/gemeenteStyle";
import {
  Kaart,
  achtergrondkaart,
  maakGeoJsonKaartlaag,
  updateKaartlaag,
  type GeoLayer,
} from "@/ts/kaartlagen";
import { jsonToNavigatie } from "@/ts/navigatie";
import {
  TOEGANKELIJKHEDEN,
  type GemeenteDataType,
  type InformatieType,
  type LegendaTextType,
  type ToegankelijkhedenID,
  type ToegankelijkheidDataTypeKey,
} from "@/ts/types";
import { computed, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";

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

// If no data present, layer will be added when data present
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
  kaart.value = new Kaart([achtergrondkaart]);
  if (toegankelijkhedenStore.isDataForVerkiezing(props.informatie.verkiezing)) {
    // If data already present add layer
    addLayer();
  }
  kaart.value.addFeatureListener((feature) => {
    featureGemeente.value = feature.get("c");
  });
});

function navigateToegankelijkeid(tg: ToegankelijkhedenID) {
  const copy = props.informatie;
  copy.toegankelijkheid = tg;
  router.replace({ query: jsonToNavigatie(copy) });
}

function handleSlider() {
  const copy = props.informatie;
  copy.percentage = percentage.value;
  router.replace({ query: jsonToNavigatie(copy) });
}

function featureGemeenteName(): string {
  if (featureGemeente.value) {
    return toegankelijkhedenStore.getGemeenteName(featureGemeente.value);
  }
  return featureGemeente.value;
}

function aanwezig(state: ToegankelijkheidDataTypeKey): number {
  const data = allData.value;
  if (data && featureGemeente.value) {
    return data[featureGemeente.value][2][toegankelijkheid.value][state] || 0;
  }
  return 0;
}

function totalGem(): number {
  const data = allData.value;
  if (data && featureGemeente.value && data[featureGemeente.value]) {
    return data[featureGemeente.value][1] || 0;
  }
  return 0;
}
const legendaText = {
  yes: "Gemeente waar de toegankelijkheid in minimaal het percentage stemlokalen aanwezig is",
  no: "Gemeenten waar in geen enkel stemlokaal de toegankelijkheid aanwezig is",
  nodata:
    "Gemeenten waar de toegankelijkheid in minder stemlokalen dan het percentage aanwezig is, of deze informatie onbekend is",
  title: true,
} as LegendaTextType;
</script>

<template>
  <div class="mapContent">
    <div class="mapSelector">
      <h2>Toegankelijkheid</h2>
      <p>Klik op een van de toegankelijkheden om de gevens op de kaart te tonen.</p>
      <button
        v-for="(tg, index) in TOEGANKELIJKHEDEN"
        :key="index"
        @click="navigateToegankelijkeid(index)"
        class="cat-link"
        :class="index == toegankelijkheid ? 'selected' : ''">
        {{ tg }}
      </button>
      <h2>Percentage</h2>
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
            <div>Ja</div>
            <div>{{ aanwezig("j") }}</div>
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
    </div>
    <Legenda :legendaText="legendaText" />
  </div>
</template>

<style scoped>
.cat-link {
  color: var(--text-color);
  width: 100%;
  margin: 10px 3px 0;
  border: none;
  text-align: left;
  background-color: transparent;
}

.cat-link::before {
  content: "•";
  margin-right: 3px;
}

.cat-link:link,
.cat-link:visited {
  text-decoration: none;
}

.cat-link:hover,
.cat-link:active {
  text-decoration: underline;
  cursor: pointer;
}

.selected {
  font-weight: bold;
}

.selected::after {
  margin-left: 3px;
  content: "✔";
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
  border-right: 1px solid #999;
}

#map {
  position: relative;
  height: calc(100vh - 72px);
  margin: 0;
  padding: 0;
}

#hover {
  position: absolute;
  display: inline-block;
  height: 210px;
  width: 200px;
  z-index: 100;
  background-color: #eee;
  color: #333;
  text-align: left;
  border-radius: 6px;
  border-color: #333;
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
  border-top: 1px solid #333;
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
</style>
