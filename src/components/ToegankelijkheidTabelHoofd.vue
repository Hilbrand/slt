<script setup lang="ts">
const props = defineProps<{
  naam: string;
}>();
</script>

<template>
  <tr class="tabel">
    <th class="cell eerste">{{ props.naam }}</th>
    <th class="cell" colspan="6">Aanwezig</th>
    <th class="cell">Onbekend</th>
    <th class="cell">Afwezig</th>
  </tr>
</template>

<style scoped>
.cell {
  border: 1px solid var(--color-tekst);
  width: 25%;
}
@media (max-width: 1024px) {
  .eerste {
    width: 120px;
  }
  th {
    font-size: 0.7em;
  }

}
</style>
