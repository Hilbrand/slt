<script setup lang="ts">
import { type ToegankelijkheidType, type ToegankelijkhedenID, TOEGANKELIJKHEDEN, TOEGANKELIJKHEDEN_IDS, Visualisatie } from "@/ts/types";
import ToegankelijkheidRegel from "@/components/ToegankelijkheidRegel.vue";
import ToegankelijkheidRegelTabel from "@/components/ToegankelijkheidRegelTabel.vue";
import ToegankelijkheidTabelHoofd from "@/components/ToegankelijkheidTabelHoofd.vue";

const props = defineProps<{
  totaal: number;
  groep: string;
  toegankelijkheden: ToegankelijkheidType;
  visualisatie: Visualisatie;
}>();

function hasData(): boolean {
  return !!props.toegankelijkheden["lb"];
}

function cat(key: ToegankelijkhedenID) {
  return (TOEGANKELIJKHEDEN[key] || "") + (key === 'to' ? " (Toegankelijk, Genderneutraal, Aanwezig)" : "");
}
</script>

<template>
  <table class="grid">
    <tbody>
      <slot />
      <template v-if="hasData()">
        <template v-if="props.visualisatie == Visualisatie.TABEL">
          <ToegankelijkheidTabelHoofd naam="Toegankelijkheid" />
          <ToegankelijkheidRegelTabel
          v-for="row in TOEGANKELIJKHEDEN_IDS"
          :key="row"
          :tid="row"
          :totaal="props.totaal"
          :groep="props.groep"
          :toegankelijkheden="props.toegankelijkheden"
          >{{ cat(row) }}</ToegankelijkheidRegelTabel>
        </template>
        <template v-else>
          <ToegankelijkheidRegel
          v-for="row in TOEGANKELIJKHEDEN_IDS"
          :key="row"
          :tid="row"
          :totaal="props.totaal"
          :groep="props.groep"
          :toegankelijkheden="props.toegankelijkheden"
          :visualisatie="props.visualisatie"
          >{{ cat(row) }}</ToegankelijkheidRegel>
        </template>
      </template>
      <tr v-else><td></td><td>Er is zijn nog geen gegevens bekend</td></tr>
    </tbody>
  </table>
</template>
