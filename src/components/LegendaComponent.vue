<script setup lang="ts">
import type { LegendaTextType } from "@/ts/types";

const props = defineProps<{
  legendaText: LegendaTextType;
}>();
</script>

<template>
  <h3 v-if="props.legendaText.titel">Legenda</h3>
  <div class="legenda">
    <div class="legenda-row">
      <div
        class="legenda-block"
        style="background-color: var(--color-ja-2)"
        aria-hidden="true"></div>
      <div class="legenda-text">{{ props.legendaText.ja }}</div>
    </div>
    <div class="legenda-row">
      <div
        class="legenda-block"
        style="background-color: var(--color-onbekend-2)"
        aria-hidden="true"></div>
      <div class="legenda-text">{{ props.legendaText.onbekend }}</div>
    </div>
    <div class="legenda-row">
      <div class="legenda-block" style="background-color: var(--color-nee-2)" aria-hidden="true"></div>
      <div class="legenda-text">{{ props.legendaText.nee }}</div>
    </div>
    <div v-if="props.legendaText.geenGegevens !== ''"
        class="legenda-row">
      <div class="legenda-block" style="background-color: var(--color-geen-gegevens)" aria-hidden="true"></div>
      <div class="legenda-text">{{ props.legendaText.geenGegevens }}</div>
    </div>
  </div>
</template>

<style scoped>
h3 {
  margin-left: 10px;
}
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
    border-bottom: 1px solid var(--color-legenda-border-bottom);
  }
}
.legenda-block {
  border: 1px solid var(--color-legenda-border);
  width: 20px;
  height: 15px;
}
.legenda-text {
  line-height: 15p;
}
</style>
