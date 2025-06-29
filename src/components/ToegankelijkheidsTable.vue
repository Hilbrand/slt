<script setup lang="ts">
import { type ToegankelijkheidType, type ToegankelijkhedenID, type ToegankelijkheidDataTypeKey, TOEGANKELIJKHEDEN, TOEGANKELIJKHEDEN_IDS } from "@/ts/types";

const props = defineProps<{
  totaal: number;
  toegankelijkheden: ToegankelijkheidType;
}>();

function hasData(): boolean {
  return !!props.toegankelijkheden["lb"];
}

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
    <template v-if="hasData()">
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
    </template>
    <tr v-else><td></td><td>Er is zijn nog geen gegevens bekend</td></tr>
  </table>
</template>
