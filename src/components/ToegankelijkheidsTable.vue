<script setup lang="ts">
import { type ToegankelijkheidType, type ToegankelijkhedenID, type ToegankelijkheidDataTypeKey, TOEGANKELIJKHEDEN, TOEGANKELIJKHEDEN_IDS } from "@/ts/types";

const props = defineProps<{
  totaal: number;
  toegankelijkheden: ToegankelijkheidType;
}>();

function width(key: ToegankelijkhedenID, state: ToegankelijkheidDataTypeKey) {
  const percentage = (show(key, state) / props.totaal) * 100;
  return "width:" + percentage + "%";
}

function cat(key: ToegankelijkhedenID) {
  return TOEGANKELIJKHEDEN[key] || "";
}

function ariaLabel(key: ToegankelijkhedenID, state: ToegankelijkheidDataTypeKey, append: string = "") {
  return "Aantal stemlokalen met " + cat(key) + append + ": " + show(key, state);
}

function show(key: ToegankelijkhedenID, state: ToegankelijkheidDataTypeKey): number {
  return props.toegankelijkheden[key] && props.toegankelijkheden[key][state]
      ? props.toegankelijkheden[key][state] : 0;
}
</script>

<template>
  <table class="grid">
    <slot />
    <tr v-for="row in TOEGANKELIJKHEDEN_IDS" :key="row">
      <td>{{ cat(row) }}</td>
      <td class="row">
        <div
          v-if="row == 'gt'"
          :aria-label="ariaLabel(row, 'l', ' op locatie')"
          class="cell yes"
          :style="width(row, 'l')">
          {{ show(row, "l") }}
        </div>
        <div
          v-if="row == 'gt'"
          :aria-label="ariaLabel(row, 'a', ' op afstand')"
          class="cell yes"
          :style="width(row, 'a')">
          {{ show(row, "a") }}
        </div>
        <div
          v-if="row != 'gt'"
          :aria-label="ariaLabel(row, 'j')"
          class="cell yes"
          :style="width(row, 'j')">
          {{ show(row, "j") }}
        </div>
        <div
          :aria-label="ariaLabel(row, '')"
          class="cell unknown"
          :style="width(row, '')">
          {{ show(row, "") }}
        </div>
        <div
          :aria-label="ariaLabel(row, 'n')"
          class="cell no"
          :style="width(row, 'n')">
          {{ show(row, 'n') }}
        </div>
      </td>
    </tr>
  </table>
</template>

<style>
.grid {
  table-layout: fixed;
  width: 100%;
  padding: 10px;
}

.grid td:first-child {
  width: 300px;
}

.row {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  margin-bottom: 0.5rem;
}

.yes {
  background-color: var(--color-yes);
  color: white;
}

.unknown {
  background-color: var(--color-unknown);
  color: #333;
}

.no {
  background-color: var(--color-no);
  color: white;
}

.cell {
  height: 30px;
  text-align: center;
  line-height: 30px;
  white-space: nowrap;
}
@media (max-width: 1024px) {
  .grid td:first-child {
    width: 50%;
  }
  .row {
    margin-bottom: 1rem;
  }
}
</style>
