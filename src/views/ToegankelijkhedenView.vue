<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import { maakGemeenteData } from "@/ts/downloadData";
import { jsonToNavigatie } from "@/ts/navigatie";
import { hoofdRegelGemeenteCsv, TOEGANKELIJKHEDEN, TOEGANKELIJKHEDEN_IDS, Visualisatie, type InformatieType, type LegendaTextType, type ToegankelijkhedenID, type ToegankelijkheidAreaType } from "@/ts/types";
import Download from "@/components/DownloadComponent.vue";
import Legenda from "@/components/LegendaComponent.vue";
import ToegankelijkheidRegel from "@/components/ToegankelijkheidRegel.vue";
import ToegankelijkheidRegelTabel from "@/components/ToegankelijkheidRegelTabel.vue";
import ToegankelijkheidTabelHoofd from "@/components/ToegankelijkheidTabelHoofd.vue";

const router = useRouter();

const props = defineProps<{
  informatie: InformatieType;
}>();

const toegankelijkhedenStore = useToegankelijkhedenStore();

const toegankelijkheidText = computed<string>(() =>
  props.informatie?.toegankelijkheid && TOEGANKELIJKHEDEN[props.informatie?.toegankelijkheid] || "",
);

const nationaal = computed<ToegankelijkheidAreaType>(() =>
  toegankelijkhedenStore.loadedVerkiezing() == props.informatie?.verkiezing
    ? toegankelijkhedenStore.getNationaal()
    : ["", 0, {}],
);

const gemeenten = computed(() =>
  toegankelijkhedenStore.isDataForVerkiezing(props.informatie?.verkiezing)
    ? toegankelijkhedenStore.getGemeenten()
    : [],
);

const csvBestandsnaam = computed(() => {
  return `${props.informatie.verkiezing}_${toegankelijkheidText.value.toLowerCase()}`;
});

function idGem(gemId: string): string {
  return `tg-${gemId}`;
}

function scrollNaarGemeente(gemId: string) {
  const element = document.getElementById(idGem(gemId));
  element?.scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => {
  scrollNaarGemeente(props.informatie.gemeente);
});

function selected(tg: string): boolean {
  return props.informatie?.toegankelijkheid === tg;
}

function navigateGemeente(gemeente: string) {
  const copy = props.informatie;
  copy.gemeente = gemeente;
  copy.pagina = "gemeente";
  router.push({ query: jsonToNavigatie(copy) });
}

function wisselToegankelijkheid(event: Event) {
  const e = event.target as HTMLInputElement;
  const copy = props.informatie;
  copy.toegankelijkheid = e.value as ToegankelijkhedenID;
  router.push({ query: jsonToNavigatie(copy) });
}

const legendaText = {
  ja: "Aantal stemlokalen waar de toegankelijkheid aanwezig is",
  nee: "Aantal stemlokalen waar de toegankelijkheid afwezig is",
  onbekend: "Aantal stemlokalen waar de toegankelijkheidsinformatie onbekend is",
  geenGegevens: "",
  titel: true,
} as LegendaTextType;
</script>

<template>
  <select class="select" @change="wisselToegankelijkheid">
    <option v-for="row in TOEGANKELIJKHEDEN_IDS" :key="row"
        :value="row"
        :selected="selected(row)">
      {{ TOEGANKELIJKHEDEN[row] }}
    </option>
  </select>
  <div class="tabel-tg">
  <Download
    :bestandsnaam="csvBestandsnaam"
    :hoofdregel="hoofdRegelGemeenteCsv"
    :regelData="() => maakGemeenteData(props.informatie.toegankelijkheid)" />
  <table class="grid">
    <tbody>
      <template v-if="props.informatie.visualisatie == Visualisatie.TABEL">
        <ToegankelijkheidTabelHoofd naam="Gemeente" />
        <ToegankelijkheidRegelTabel
          :id="nationaal[0]"
          :tid="props.informatie.toegankelijkheid"
          groep="stemlokalen"
          :toegankelijkheden="nationaal[2]">
          {{ toegankelijkhedenStore.getGemeenteName(nationaal[0]) }}
        </ToegankelijkheidRegelTabel>
        <ToegankelijkheidRegelTabel
          v-for="gem in gemeenten"
          :id="idGem(gem[0])"
          :key="gem[0]"
          :tid="props.informatie.toegankelijkheid"
          groep="stemlokalen"
          :toegankelijkheden="toegankelijkhedenStore.getToegankelijkheden(gem[0])"
          ><a @click=navigateGemeente(gem[0])>{{  gem[1] }}</a>
        </ToegankelijkheidRegelTabel>
      </template>
      <template v-else>
         <ToegankelijkheidRegel
          :toegankelijkheid="toegankelijkheidText"
          :tid="props.informatie.toegankelijkheid"
          :totaal="nationaal[1]"
          groep="stemlokalen"
          :toegankelijkheden="nationaal[2]">Alle stemlokalen</ToegankelijkheidRegel>
        <ToegankelijkheidRegel
          v-for="gem in gemeenten"
          :id="idGem(gem[0])"
          :key="gem[0]"
          :toegankelijkheid="toegankelijkheidText"
          :tid="props.informatie.toegankelijkheid"
          :totaal="toegankelijkhedenStore.getStemlokalen(gem[0])"
          groep="stemlokalen"
          :toegankelijkheden="toegankelijkhedenStore.getToegankelijkheden(gem[0])"
          :visualisatie="props.informatie.visualisatie">
          <a @click=navigateGemeente(gem[0])>{{  gem[1] }}</a>
        </ToegankelijkheidRegel>
        </template>
    </tbody>
  </table>
  <Legenda v-if="props.informatie.visualisatie == Visualisatie.GRAFIEK"
    :legendaText="legendaText" />
  </div>
</template>

<style scoped>
.grid tr {
  scroll-margin-top: 140px;
}
@media (max-width: 1024px) {
  .grid tr {
    scroll-margin-top: 120px;
  }
}
</style>
