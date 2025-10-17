<script setup lang="ts">
import { type ToegankelijkheidType, type ToegankelijkhedenID, TOEGANKELIJKHEDEN, TOEGANKELIJKHEDEN_IDS } from "@/ts/types";
import ToegankelijkheidRegel from "@/components/ToegankelijkheidRegel.vue";

const props = defineProps<{
  totaal: number;
  groep: string;
  toegankelijkheden: ToegankelijkheidType;
}>();

function hasData(): boolean {
  return !!props.toegankelijkheden["lb"];
}

function cat(key: ToegankelijkhedenID) {
  return TOEGANKELIJKHEDEN[key] || "";
}
</script>

<template>
  <table class="grid">
    <tbody>
      <slot />
      <template v-if="hasData()">
        <ToegankelijkheidRegel
          v-for="row in TOEGANKELIJKHEDEN_IDS"
          :key="row"
          :tid="row"
          :totaal="props.totaal"
          :groep="props.groep"
          :toegankelijkheden="props.toegankelijkheden"
          >{{ cat(row) }}</ToegankelijkheidRegel>
      </template>
      <tr v-else><td></td><td>Er is zijn nog geen gegevens bekend</td></tr>
    </tbody>
  </table>
</template>

