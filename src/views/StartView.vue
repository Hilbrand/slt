<script setup lang="ts">
import { computed } from "vue";
import type { InformatieType, LegendaTextType, ToegankelijkheidAreaType } from "@/ts/types";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import Legenda from "@/components/LegendaComponent.vue";
import ToegankelijkheidsTable from "@/components/ToegankelijkheidsTable.vue";

const props = defineProps<{
  informatie: InformatieType;
}>();

const toegankelijkhedenStore = useToegankelijkhedenStore();

const national = computed<ToegankelijkheidAreaType>(() =>
  toegankelijkhedenStore.loadedVerkiezing() == props.informatie?.verkiezing
    ? toegankelijkhedenStore.getNational()
    : ["", 0, []],
);
const atLeastOne = computed<ToegankelijkheidAreaType>(() =>
  toegankelijkhedenStore.loadedVerkiezing() == props.informatie?.verkiezing
    ? toegankelijkhedenStore.getAtLeastOne()
    : ["", 0, []],
);
const alleToegankelijkheid = {
  yes: "Stemlokalen waar de toegankelijkheid aanwezig is",
  no: "Stemlokalen waar toegankelijkheid afwezig is",
  nodata: "Stemlokalen waar geen gegevens van zijn",
} as LegendaTextType;

const atLeastOneToegankelijkheid = {
  yes: "Aantal gemeenten waar minimaal in 1 stemlokaal de toegankelijkheid aanwezig is",
  no: "Aantal gemeenten waar de toegankelijkheid in geen enkel stemlokaal aanwezig is",
  nodata: "Aantal gemeenten waar geen gegevens voor toegankelijkheid zijn opgegeven",
} as LegendaTextType;
</script>

<template v-if="national !== undefined">
  <h3>Toegankelijkheid van alle stembureaus</h3>
  <ToegankelijkheidsTable :totaal="national[1]" :toegankelijkheden="national[2]">
    <tr>
      <td>Aantal Stemlokalen</td>
      <td class="row">
        <div class="cell yes" style="width: 100%">{{ national[1] }}</div>
      </td>
    </tr>
  </ToegankelijkheidsTable>
  <div class="legenda">
    <Legenda :legendaText="alleToegankelijkheid" />
  </div>
  <h3>Gemeenten waar minimaal 1 stemlokaal de toegankelijkheid aanwezig is</h3>
  <ToegankelijkheidsTable :totaal="atLeastOne[1]" :toegankelijkheden="atLeastOne[2]">
    <tr>
      <td>Aantal Gemeenten</td>
      <td class="row">
        <div class="cell yes" style="width: 100%">{{ atLeastOne[1] }}</div>
      </td>
    </tr>
  </ToegankelijkheidsTable>
  <div class="legenda">
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
