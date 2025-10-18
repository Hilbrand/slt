<script setup lang="ts">
import { type ToegankelijkheidType, type ToegankelijkhedenID, type ToegankelijkheidDataTypeKey, TOEGANKELIJKHEDEN } from "@/ts/types";

const props = defineProps<{
  tid: ToegankelijkhedenID,
  totaal: number;
  groep: string;
  toegankelijkheden: ToegankelijkheidType;
}>();

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
  return `Aantal ${props.groep} met ${cat(props.tid)}${append}: ${show(key, state)}`;
}

</script>

<template>
  <tr>
    <td><slot /></td>
    <td class="row">
      <div
        v-if="tid == 'gt' && show(tid, 'l') > 0"
        :title="titleLabel(tid, 'l', ' op locatie aanwezig')"
        class="cell yes ola"
        :class="`${tekortJa(tid, 'l')} ${tekortJaKlein(tid, 'l')}` "
        :style="width(tid, 'l')">
        {{ show(tid, "l") }}
      </div>
      <div
        v-if="tid == 'gt' && show(tid, 'a') > 0"
        :title="titleLabel(tid, 'a', ' op afstand aanwezig')"
        class="cell yes"
        :class="`${tekortJa(tid, 'a')} ${tekortJaKlein(tid, 'a')}` "
        :style="width(tid, 'a')">
        {{ show(tid, "a") }}
      </div>
      <div
        v-if="tid != 'gt' && show(tid, 'j') > 0"
        :title="titleLabel(tid, 'j', ' aanwezig')"
        class="cell yes"
        :class="`${tekortJa(tid, 'j')} ${tekortJaKlein(tid, 'j')}` "
        :style="width(tid, 'j')">
        {{ show(tid, "j") }}
      </div>
      <div
        v-if="show(tid, '') > 0"
        :title="titleLabel(tid, '', ' onbekend')"
        class="cell unknown"
        :style="width(tid, '')">
        {{ show(tid, "") }}
      </div>
      <div
        v-if="show(tid, 'n') > 0"
        :title="titleLabel(tid, 'n', ' afwezig')"
        class="cell no"
        :class="tekort(tid, 'n')"
        :style="width(tid, 'n')">
        {{ show(tid, 'n')  }}
      </div>
    </td>
  </tr>
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
