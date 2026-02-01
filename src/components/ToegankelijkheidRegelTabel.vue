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
  <tr v-if="props.toegankelijkheden[tid] !== undefined"
    class="tabel">
    <td><slot /></td>
    <td
      :title="titleLabel(tid, 'j', ' aanwezig')"
      class="cell">
      {{ show(tid, "j") }}
    </td>
    <td
      :title="titleLabel(tid, '', ' onbekend')"
      class="cell"
      >
      {{ show(tid, "") }}
    </td>
    <td
      :title="titleLabel(tid, 'n', ' afwezig')"
      class="cell">
      {{ show(tid, 'n')  }}
    </td>
  </tr>
</template>

<style scoped>
</style>
