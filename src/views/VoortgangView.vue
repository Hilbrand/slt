<script setup lang="ts">
import { type InformatieType } from "@/ts/types";
import { leesCsv, maakGrafiek, type GemeentenGepubliceerdItem } from "@/ts/voortgangGrafiek";
import { onMounted, onUnmounted, ref, watch } from "vue";

const props = defineProps<{
  informatie: InformatieType;
}>();

const ggGrafiek = ref(null);
const gegevens = ref<GemeentenGepubliceerdItem[] | null>(null);

async function tekenGrafiek() {
  const verkiezing = props.informatie.verkiezing;

  if (verkiezing != null && gegevens.value == null) {
    gegevens.value = await leesCsv(verkiezing);
  }
  if (ggGrafiek.value !== null && gegevens.value != null) {
    maakGrafiek(verkiezing, gegevens.value, ggGrafiek.value, window.innerWidth);
  }
}

watch(
  () => ggGrafiek,
  (newState) => {
    if (newState.value) {
      tekenGrafiek();
    }
  },
  { immediate: true, deep: true },
);

function resize() {
  tekenGrafiek();
}

onMounted(() => {
  window.addEventListener("resize", resize);
});
onUnmounted(() => {
  window.removeEventListener("resize", resize);
});
</script>

<template>
  <div class="midden">
    <h3>Aantal gemeenten die gegevens hebben gepubliceerd</h3>
    <div style="margin-left: 10px" ref="ggGrafiek"></div>
  </div>
</template>

<style scoped>
.midden {
  width: 100%;
  display: grid;
  vertical-align: center;
}
.midden > * {
  justify-self: center;
}
</style>
