<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { jsonToNavigatie } from "@/ts/navigatie";
import { TOEGANKELIJKHEDEN, TOEGANKELIJKHEDEN_IDS, type InformatieType, type LegendaTextType, type ToegankelijkhedenID, type ToegankelijkheidAreaType, type ToegankelijkheidType } from "@/ts/types";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import Legenda from "@/components/LegendaComponent.vue";
import ToegankelijkheidsTable from "@/components/ToegankelijkheidsTable.vue";
import ToegankelijkheidRegel from "@/components/ToegankelijkheidRegel.vue";
import { preventDefault } from "ol/events/Event";

const router = useRouter();

const props = defineProps<{
  informatie: InformatieType;
}>();

const toegankelijkhedenStore = useToegankelijkhedenStore();

// const toegankelijkheid = ref<ToegankelijkhedenID>("lb");
const toegankelijkheidText = computed<string>(() =>
  props.informatie?.toegankelijkheid && TOEGANKELIJKHEDEN[props.informatie?.toegankelijkheid] || "",
);

const nationaal = computed<ToegankelijkheidAreaType>(() =>
  toegankelijkhedenStore.loadedVerkiezing() == props.informatie?.verkiezing
    ? toegankelijkhedenStore.getNational()
    : ["", 0, {}],
);

const gemeenten = computed(() =>
  toegankelijkhedenStore.isDataForVerkiezing(props.informatie?.verkiezing)
    ? toegankelijkhedenStore.getGemeenten()
    : [],
);

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
  <div class="tabel">
  <table class="grid">
    <tbody>
      <ToegankelijkheidRegel
        :toegankelijkheid="toegankelijkheidText"
        :tid="props.informatie.toegankelijkheid"
        :totaal="nationaal[1]"
        groep="gemeenten"
        :toegankelijkheden="nationaal[2]">Alle stemlokalen</ToegankelijkheidRegel>
      <ToegankelijkheidRegel
        v-for="gem in gemeenten"
        :key="gem[0]"
        :toegankelijkheid="toegankelijkheidText"
        :tid="props.informatie.toegankelijkheid"
        :totaal="toegankelijkhedenStore.getStemlokalen(gem[0])"
        groep="gemeenten"
        :toegankelijkheden="toegankelijkhedenStore.getToegankelijkheden(gem[0])">
        <a @click=navigateGemeente(gem[0])>{{  gem[1] }}</a>
      </ToegankelijkheidRegel>
    </tbody>
  </table>
  <Legenda :legendaText="legendaText" />
  </div>
</template>

<style scoped>
.select {
  border-radius: 5px;
  position: fixed;
  top: 100px;
  margin-left: 10px;
  z-index: 10000;
}

@media (max-width: 1024px) {
  .select {
    top: 80px;
    right: 10px;
    width: 50%;
  }
}
</style>
