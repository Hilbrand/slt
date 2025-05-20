<script setup lang="ts">
import { color_unknown } from "@/ts/gemeenteStyle";
import type { LegendaTextType } from "@/ts/types";

const props = defineProps<{
  legendaText: LegendaTextType;
}>();
</script>

<template>
  <h3 v-if="props.legendaText.title">Legenda</h3>
  <div class="legenda">
    <div class="legenda-row">
      <div
        class="legenda-block"
        style="background-color: var(--color-yes)"
        aria-hidden="true"></div>
      <div class="legenda-text">{{ props.legendaText.yes }}</div>
    </div>
    <div class="legenda-row">
      <div
        class="legenda-block"
        :style="'background-color:' + color_unknown"
        aria-hidden="true"></div>
      <div class="legenda-text">{{ props.legendaText.nodata }}</div>
    </div>
    <div class="legenda-row">
      <div class="legenda-block" style="background-color: var(--color-no)" aria-hidden="true"></div>
      <div class="legenda-text">{{ props.legendaText.no }}</div>
    </div>
  </div>
</template>

<style scoped>
.legenda-row {
  display: grid;
  grid-template-columns: 2em 1fr;
  align-items: center;
  margin: 10px;
}
@media (min-width: 512px) {
  .legenda {
    display: flex;
    justify-content: space-between;
    margin: 0 10px 30px 10px;
    border-bottom: 1px solid #333;
  }
}
.legenda-block {
  border: 1px solid #aaa;
  width: 20px;
  height: 15px;
}
.legenda-text {
  line-height: 15p;
}
</style>
