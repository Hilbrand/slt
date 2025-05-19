<script setup lang="ts">
import { color_unknown } from "@/ts/gemeenteStyle";
import type { LegendaTextType } from "@/ts/types";

const props = defineProps<{
  legendaText: LegendaTextType;
}>();
</script>

<template>
  <h3 v-if="props.legendaText.title">Legenda</h3>
  <div class="leganda-row">
    <div class="leganda-block" style="background-color: var(--color-yes)" aria-hidden="true"></div>
    <div>{{ props.legendaText.yes }}</div>
  </div>
  <div class="leganda-row">
    <div
      class="leganda-block"
      :style="'background-color:' + color_unknown"
      aria-hidden="true"></div>
    <div>{{ props.legendaText.nodata }}</div>
  </div>
  <div class="leganda-row">
    <div class="leganda-block" style="background-color: var(--color-no)" aria-hidden="true"></div>
    <div>{{ props.legendaText.no }}</div>
  </div>
</template>

<style scoped>
.leganda-row {
  display: grid;
  margin: 10px 0;
  grid-template-columns: 2em auto;
}

.leganda-block {
  border: 1px solid #aaa;
  width: 20px;
  height: 10px;
}
</style>
