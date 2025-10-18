<script setup lang="ts">
import { computed } from "vue";
import { Visualisatie, type InformatieType, type LegendaTextType, type ToegankelijkheidAreaType } from "@/ts/types";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import Legenda from "@/components/LegendaComponent.vue";
import ToegankelijkheidsTable from "@/components/ToegankelijkheidsTable.vue";
import ToegankelijkheidTabelHoofd from "@/components/ToegankelijkheidTabelHoofd.vue";

const props = defineProps<{
  informatie: InformatieType;
}>();

const toegankelijkhedenStore = useToegankelijkhedenStore();

const nationaal = computed<ToegankelijkheidAreaType>(() =>
  toegankelijkhedenStore.loadedVerkiezing() == props.informatie?.verkiezing
    ? toegankelijkhedenStore.getNational()
    : ["", 0, {}],
);
const atLeastOne = computed<ToegankelijkheidAreaType>(() =>
  toegankelijkhedenStore.loadedVerkiezing() == props.informatie?.verkiezing
    ? toegankelijkhedenStore.getAtLeastOne()
    : ["", 0, {}],
);
const alleToegankelijkheid = {
  ja: "Stemlokalen waar de toegankelijkheid aanwezig is",
  nee: "Stemlokalen waar toegankelijkheid afwezig is",
  onbekend: "Stemlokalen waar geen gegevens van zijn",
  geenGegevens: "",
} as LegendaTextType;

const grafiek = computed(() => {
  return props.informatie.visualisatie == Visualisatie.GRAFIEK;
});

const atLeastOneToegankelijkheid = {
  ja: "Aantal gemeenten waar minimaal in 1 stemlokaal de toegankelijkheid aanwezig is",
  nee: "Aantal gemeenten waar de toegankelijkheid in geen enkel stemlokaal aanwezig is",
  onbekend: "Aantal gemeenten waar geen gegevens voor toegankelijkheid zijn opgegeven",
  geenGegevens: "",
} as LegendaTextType;
</script>

<template v-if="national !== undefined">
  <h3>Toegankelijkheid van alle stembureaus</h3>
  <div v-if="!grafiek"
    class="totaal-tekst">Aantal stemlokalen: {{ nationaal[1] }}</div>
  <ToegankelijkheidsTable
    :totaal="nationaal[1]"
    groep="stemlokalen"
    :toegankelijkheden="nationaal[2]"
    :visualisatie="props.informatie.visualisatie">
    <tr v-if="grafiek">
      <td>Aantal Stemlokalen</td>
      <td class="row">
        <div class="cell yes" style="width: 100%">{{ nationaal[1] }}</div>
      </td>
    </tr>
  </ToegankelijkheidsTable>
  <div v-if="grafiek"
    class="legenda">
    <Legenda :legendaText="alleToegankelijkheid" />
  </div>
  <h3>Gemeenten waar minimaal 1 stemlokaal de toegankelijkheid aanwezig is</h3>
  <div v-if="!grafiek"
    class="totaal-tekst">Aantal gemeenten: {{ atLeastOne[1] }}</div>
  <ToegankelijkheidsTable
    :totaal="atLeastOne[1]"
    groep="gemeenten"
    :toegankelijkheden="atLeastOne[2]"
    :visualisatie="props.informatie.visualisatie">
    <tr v-if="grafiek">
      <td>Aantal Gemeenten</td>
      <td class="row">
        <div class="cell yes" style="width: 100%">{{ atLeastOne[1] }}</div>
      </td>
    </tr>
  </ToegankelijkheidsTable>
  <div v-if="grafiek"
    class="legenda" >
    <Legenda :legendaText="atLeastOneToegankelijkheid" />
  </div>
</template>

<style scoped>
h3 {
  text-align: center;
  width: 100%;
}
.legenda h3 {
  display: none;
}
</style>
