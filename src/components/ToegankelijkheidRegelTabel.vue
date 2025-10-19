<script setup lang="ts">
import { type ToegankelijkheidType, type ToegankelijkhedenID, type ToegankelijkheidDataTypeKey, TOEGANKELIJKHEDEN } from "@/ts/types";

const props = defineProps<{
  tid: ToegankelijkhedenID,
  groep: string;
  toegankelijkheden: ToegankelijkheidType;
}>();

function show(key: ToegankelijkhedenID, state: ToegankelijkheidDataTypeKey): number {
  return props.toegankelijkheden[key] && props.toegankelijkheden[key][state] || 0;
}

function cat(key: ToegankelijkhedenID) {
  return TOEGANKELIJKHEDEN[key] || "";
}

function titleLabel(key: ToegankelijkhedenID, state: ToegankelijkheidDataTypeKey, append: string = "") {
  return `Aantal ${props.groep} met ${cat(props.tid)}${append}: ${show(key, state)}`;
}
</script>

<template>
  <tr class="tabel">
    <td><slot /></td>
    <!-- <td class="row"> -->
    <td
      v-if="tid == 'gt'"
      :title="titleLabel(tid, 'l', ' op locatie aanwezig')"
      class="cell"
      style="width:12.5%">
      {{ show(tid, "l") }}
    </td>
    <td
      v-if="tid == 'gt'"
      :title="titleLabel(tid, 'a', ' op afstand aanwezig')"
      class="cell"
      style="width:12.5%">
      {{ show(tid, "a") }}
    </td>
    <td
      v-if="tid != 'gt'"
      colspan="2"
      :title="titleLabel(tid, 'j', ' aanwezig')"
      class="cell"
      style="width:25%">
      {{ show(tid, "j") }}
    </td>
    <td
      :title="titleLabel(tid, '', ' onbekend')"
      class="cell"
      style="width:25%">
      {{ show(tid, "") }}
    </td>
    <td
      :title="titleLabel(tid, 'n', ' afwezig')"
      class="cell"
      style="width:25%">
      {{ show(tid, 'n')  }}
    </td>
  </tr>
</template>

<style scoped>
</style>
