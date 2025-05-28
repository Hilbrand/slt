<script setup lang="ts">
import { computed } from "vue";
import type { InformatieType, LegendaTextType } from "@/ts/types";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import Legenda from "@/components/LegendaComponent.vue";
import {
  ANDERE_NAAM,
  ANDERE_NAAM_PERCENTAGE,
  ANDERE_POSTCODE,
  ANDERE_POSTCODE_PERCENTAGE,
  CODE,
  useEmlMismatchesStore,
  ZELFDE,
  ZELFDE_PERCENTAGE,
  type GemeenteMismatch,
} from "@/stores/emlMismatchesStore";

const props = defineProps<{
  informatie: InformatieType;
}>();

const toegankelijkhedenStore = useToegankelijkhedenStore();
const emlMismatchesStore = useEmlMismatchesStore();

const alles = computed<GemeenteMismatch[]>(() =>
  emlMismatchesStore.loadedVerkiezing() == props.informatie?.verkiezing
    ? emlMismatchesStore.getAll()
    : [],
);

function show(row: GemeenteMismatch, index: number) {
  const aantal = row[index];
  return aantal == 0 ? "" : aantal;
}

function width(row: GemeenteMismatch, index: number) {
  return "width:" + row[index] + "%";
}

function cat(key: GemeenteMismatch) {
  return toegankelijkhedenStore.getGemeenteName(key[CODE]) || "";
}

function ariaLabel(key: GemeenteMismatch, index: number, append: string = "") {
  return "Aantal stemlokalen met " + cat(key) + append + ": " + show(key, index);
}

const emlDataLegenda = {
  no: "Aantal stemlokalen waar de naam van stemlokaal in de EML data verschilt met de naam in WaarIsMijnStemlokaal",
  nodata:
    "Aantal stemlokalen waar de postcode van het stemlokaal in de EML data verschilt met de naam in WaarIsMijnStemlokaal",
  yes: "Aantal stemlokalen waar de naam van het stemlokaal in de EML data hetzelfde is als de naam in WaarIsMijnStemlokaal",
} as LegendaTextType;
</script>

<template>
  <h3>Niet overeenkomende data EML/waarismijnstemlokaal</h3>
  <p class="tekst">
    Voor journalisten en onderzoekers zijn de verkiezingsuitslagen zoals gepubliceerd door de
    Kiesraad en de gegevens van WaarIsMijnStemlokaal 2 bronnen om onderzoek te doen,
    of uitslagen op een kaart te visualiseren.
    Om dit mogelijk te maken is het nodig om stemlokaties uit de verkiezingsuitslagen te kunnen
    matchen met de stemlokaties van WaarIsMijnStemlokaal.
    In het meest ideale geval kan deze match gebeuren op het stemlokaalnummer.
    Echter die nummers komen niet allemaal overeen.
    In deze tabel is een overzicht van in elke plaats hoeveel stemlokalen niet overeenkomen.
    Er is naar 2 verschillen gekeken:
  </p>
  <ul class="tekst">
    <li>Verschillende stemlokaalnaam &dash;
    Oorzaak kan zijn verkeerde nummering, naam in EML, straatnaam in WaarIsMijnStemLokaal, typos in naam</li>
    <li>Verschillende postcode &dash;
    In EML wordt vaak in de naam ook de postcode vermeld. Wanneer de stemlokaties naam hetzelfde is,
      maar de in beide opgegeven postcodes zijn verschillend wordt dit al verschil aangemerkt.
      Een stemlokaal waar de naam niet overeenkomt, en de postcode ook niet overeenkomt wordt alleen als niet overeenkomende naam gemeld.</li>
  </ul>
  <div class="legenda">
    <Legenda :legendaText="emlDataLegenda" />
  </div>
  <table class="grid">
    <tr v-for="row in alles" :key="row[0]">
      <td>{{ cat(row) }}</td>
      <td class="row">
        <div
          :aria-label="ariaLabel(row, ANDERE_NAAM)"
          class="cell no"
          :style="width(row, ANDERE_NAAM_PERCENTAGE)">
          {{ show(row, ANDERE_NAAM) }}
        </div>
        <div
          :aria-label="ariaLabel(row, ANDERE_POSTCODE)"
          class="cell unknown"
          :style="width(row, ANDERE_POSTCODE_PERCENTAGE)">
          {{ show(row, ANDERE_POSTCODE) }}
        </div>
        <div
          :aria-label="ariaLabel(row, ZELFDE)"
          class="cell yes"
          :style="width(row, ZELFDE_PERCENTAGE)">
          {{ show(row, ZELFDE) }}
        </div>
      </td>
    </tr>
  </table>
</template>

<style scoped>
h3 {
  text-align: center;
  width: 100%;
}
.legenda h3 {
  display: none;
}
.tekst {
  margin: 15px;
}
.grid {
  table-layout: fixed;
  width: 100%;
  padding: 10px;
}
.grid td:first-child {
  width: 300px;
}

.row {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  margin-bottom: 0.5rem;
}
</style>
