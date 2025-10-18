<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { jsonToNavigatie } from "@/ts/navigatie";
import { Visualisatie, type InformatieType, type LegendaTextType, type ToegankelijkheidType } from "@/ts/types";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import Legenda from "@/components/LegendaComponent.vue";
import ToegankelijkheidsTable from "@/components/ToegankelijkheidsTable.vue";

const router = useRouter();

const props = defineProps<{
  informatie: InformatieType;
}>();

const toegankelijkhedenStore = useToegankelijkhedenStore();

const totaal = computed<number>(() =>
  toegankelijkhedenStore.isDataForVerkiezing(props.informatie?.verkiezing)
    ? toegankelijkhedenStore.getStemlokalen(props.informatie?.gemeente)
    : 0,
);

const toegankelijkheden = computed<ToegankelijkheidType>(() =>
  toegankelijkhedenStore.isDataForVerkiezing(props.informatie?.verkiezing)
    ? toegankelijkhedenStore.getToegankelijkheden(props.informatie?.gemeente)
    : {},
);

const gemeenten = computed(() =>
  toegankelijkhedenStore.isDataForVerkiezing(props.informatie?.verkiezing)
    ? toegankelijkhedenStore.getGemeenten()
    : [],
);

function selected(gem: string): boolean {
  return props.informatie?.gemeente === gem;
}

function wisselGemeente(event: Event) {
  const e = event.target as HTMLInputElement;
  const copy = props.informatie;
  copy.gemeente = e.value;
  router.push({ query: jsonToNavigatie(copy) });
}

const grafiek = computed(() => {
  return props.informatie.visualisatie == Visualisatie.GRAFIEK;
});

const legendaText = {
  ja: "Aantal stemlokalen waar de toegankelijkheid aanwezig is",
  nee: "Aantal stemlokalen waar de toegankelijkheid afwezig is",
  onbekend: "Aantal stemlokalen waar de toegankelijkheidsinformatie onbekend is",
  geenGegevens: "",
  titel: true,
} as LegendaTextType;
</script>

<template v-if="toegankelijkheden !== undefined">
  <select class="select" @change="wisselGemeente">
    <option>Selecteer een gemeente</option>
    <option v-for="gem in gemeenten" :key="gem[0]"
        :value="gem[0]"
        :selected="selected(gem[0])">
      {{ gem[1] }}
    </option>
  </select>
  <div v-if="!grafiek"
    class="totaal-tekst">Aantal stemlokalen: {{ totaal }}</div>
  <ToegankelijkheidsTable
    :totaal="totaal"
    groep="stemlokalen"
    :toegankelijkheden="toegankelijkheden"
    :visualisatie="props.informatie.visualisatie">
    <tr v-if="grafiek">
      <td>Aantal stemlokalen</td>
      <td v-if="grafiek"
        class="row">
        <div class="cell yes" style="width: 100%">{{ totaal }}</div>
      </td>
    </tr>
  </ToegankelijkheidsTable>
  <Legenda v-if="grafiek"
    :legendaText="legendaText" />
</template>

<style scoped>
.select {
  z-index: 10000;
  margin:10px;
}
@media (max-width: 1024px) {
  .select {
    position: fixed;
    top: 78px;
    right: 5px;
    width: 50%;
    margin: 0px;
  }
}
</style>
