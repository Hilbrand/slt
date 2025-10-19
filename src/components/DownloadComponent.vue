<script setup lang="ts">
import type { RegelDataCsv } from '@/ts/types';
import { computed, ref } from 'vue';

const props = defineProps<{
  bestandsnaam: string;
  hoofdregel: string[];
  regelData: RegelDataCsv;
}>();

const anchor = ref();
const bestandsnaam = computed(() => `toegankelijkheid_${props.bestandsnaam}.csv`);

function maakBestandInhoud() {
  const csvInHoud =
    [props.hoofdregel.join(','),
      ...props.regelData().map(row => row.join(','))
  ].join('\n');
  const blob = new Blob([csvInHoud], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);

  if (anchor.value) {
    anchor.value.href = url;
  }
}
</script>

<template>
  <a ref="anchor"
    :download=bestandsnaam
    class="download"
    target="_blank"
    :title="`Download ${bestandsnaam}`"
    @click="maakBestandInhoud()">Download csv</a>
</template>

<style scoped>
</style>