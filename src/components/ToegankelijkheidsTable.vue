<script setup lang="ts">
import { type ToegankelijkheidType, type ToegankelijkhedenID, type ToegankelijkheidDataTypeKey, TOEGANKELIJKHEDEN, TOEGANKELIJKHEDEN_IDS } from "@/ts/types";

const props = defineProps<{
  totaal: number;
  groep: string;
  toegankelijkheden: ToegankelijkheidType;
}>();

function hasData(): boolean {
  return !!props.toegankelijkheden["lb"];
}

function show(key: ToegankelijkhedenID, state: ToegankelijkheidDataTypeKey): number {
  return props.toegankelijkheden[key] && props.toegankelijkheden[key][state] || 0;
}

function percentage(key: ToegankelijkhedenID, state: ToegankelijkheidDataTypeKey) {
  return (show(key, state) / props.totaal) * 100;
}

function width(key: ToegankelijkhedenID, state: ToegankelijkheidDataTypeKey) {
  return "width:" + percentage(key, state) + "%";
}

function tekort(key: ToegankelijkhedenID, state: ToegankelijkheidDataTypeKey) {
  return percentage(key, state) < 8 ? 'tekort' : '';
}

function tekortJa(key: ToegankelijkhedenID, state: ToegankelijkheidDataTypeKey) {
  return percentage(key, state) < 2 ? 'tekort-ja' : '';
}

function tekortJaKlein(key: ToegankelijkhedenID, state: ToegankelijkheidDataTypeKey) {
  return percentage(key, state) < 7 ? 'tekort-ja-klein' : '';
}

function cat(key: ToegankelijkhedenID) {
  return TOEGANKELIJKHEDEN[key] || "";
}

function titleLabel(key: ToegankelijkhedenID, state: ToegankelijkheidDataTypeKey, append: string = "") {
  return "Aantal " + props.groep + " met " + cat(key) + append + ": " + show(key, state);
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
            v-if="row == 'gt' && show(row, 'l') > 0"
            :title="titleLabel(row, 'l', ' op locatie aanwezig')"
            class="cell yes ola"
            :class="`${tekortJa(row, 'l')} ${tekortJaKlein(row, 'l')}` "
            :style="width(row, 'l')">
            {{ show(row, "l") }}
          </div>
          <div
            v-if="row == 'gt' && show(row, 'a') > 0"
            :title="titleLabel(row, 'a', ' op afstand aanwezig')"
            class="cell yes"
            :class="`${tekortJa(row, 'a')} ${tekortJaKlein(row, 'a')}` "
            :style="width(row, 'a')">
            {{ show(row, "a") }}
          </div>
          <div
            v-if="row != 'gt' && show(row, 'j') > 0"
            :title="titleLabel(row, 'j', ' aanwezig')"
            class="cell yes"
            :class="`${tekortJa(row, 'j')} ${tekortJaKlein(row, 'j')}` "
            :style="width(row, 'j')">
            {{ show(row, "j") }}
          </div>
          <div
            v-if="show(row, '') > 0"
            :title="titleLabel(row, '', ' onbekend')"
            class="cell unknown"
            :style="width(row, '')">
            {{ show(row, "") }}
          </div>
          <div
            v-if="show(row, 'n') > 0"
            :title="titleLabel(row, 'n', ' afwezig')"
            class="cell no"
            :class="tekort(row, 'n')"
            :style="width(row, 'n')">
            {{ show(row, 'n')  }}
          </div>
        </td>
      </tr>
    </template>
    <tr v-else><td></td><td>Er is zijn nog geen gegevens bekend</td></tr>
  </table>
</template>

<style scoped>
.yes, .no {
  z-index: 2;
}
.tekort-ja {
 color: var(--color-tekst-onbekend);
}
@media (max-width: 1000px) {
  .tekort-ja-klein {
    color: var(--color-tekst-onbekend);
  }
}
.ola {
  z-index: 3;
}
.no {
  display: inline-flex;
  justify-content: center;
}
@media (max-width: 1000px) {
  .tekort {
    color: var(--color-tekst-onbekend);
    justify-content: end;
  }
}
</style>
