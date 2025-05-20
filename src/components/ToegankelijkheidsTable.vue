<script setup lang="ts">
import { type ToegankelijkheidType, type ToegankelijkhedenID, TOEGANKELIJKHEDEN } from "@/ts/types";

const props = defineProps<{
  totaal: number;
  toegankelijkheden: ToegankelijkheidType[];
}>();

function width(value: number = 0) {
  const percentage = (value / props.totaal) * 100;
  return "width:" + percentage + "%";
}

function cat(key: ToegankelijkhedenID) {
  return TOEGANKELIJKHEDEN[key] || "";
}

function ariaLabel(key: ToegankelijkhedenID, value: number = 0, append: string = "") {
  return "Aantal stemlokalen met " + cat(key) + append + ": " + value;
}

function show(value: number = 0) {
  return value;
}
</script>

<template>
  <table class="grid">
    <slot />
    <tr v-for="row in toegankelijkheden">
      <td>{{ cat(row[0]) }}</td>
      <td class="row">
        <div
          v-if="row[0] == 'gt'"
          :aria-label="ariaLabel(row[0], row[1]['l'], ' op locatie')"
          class="cell yes"
          :style="width(row[1]['l'])">
          {{ show(row[1]["l"]) }}
        </div>
        <div
          v-if="row[0] == 'gt'"
          :aria-label="ariaLabel(row[0], row[1]['a'], ' op afstand')"
          class="cell yes"
          :style="width(row[1]['a'])">
          {{ show(row[1]["a"]) }}
        </div>
        <div
          v-if="row[0] != 'gt'"
          :aria-label="ariaLabel(row[0], row[1].j)"
          class="cell yes"
          :style="width(row[1]['j'])">
          {{ show(row[1]["j"]) }}
        </div>
        <div
          :aria-label="ariaLabel(row[0], row[1][''])"
          class="cell unknown"
          :style="width(row[1][''])">
          {{ show(row[1][""]) }}
        </div>
        <div
          :aria-label="ariaLabel(row[0], row[1]['n'])"
          class="cell no"
          :style="width(row[1]['n'])">
          {{ show(row[1]["n"]) }}
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
