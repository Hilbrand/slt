<script setup lang="ts">
import { DEFAULT_VERKIEZING, VERKIEZINGEN, type InformatieType } from "@/ts/types";
import { leesCsv, maakGrafiek, type GemeentenGepubliceerdItem } from "@/ts/voortgangGrafiek";
import { onMounted, onUnmounted, ref, watch } from "vue";

const props = defineProps<{
  informatie: InformatieType;
}>();

const ggGrafiek = ref(null);
const gegevens = ref<GemeentenGepubliceerdItem[] | null>(null);
const ontbrekendeGemeenten = ref<string[] | null>(null);

async function leesOntbrekendeGemeentenCsv(verkiezing: string): Promise<string[]> {
  try {
    const data = await fetch(verkiezing + "_ontbrekende_gemeenten.csv");
    const gemeenten = await data.text();

    if (gemeenten.includes('html')) {
      return [];
    }
    return gemeenten.split('\n');
  } catch(error) {
    console.log("Fout bij laden ontbrekende gemeenten:", error);
    return [];
  }
}

async function tekenGrafiek() {
  const verkiezing = DEFAULT_VERKIEZING;
  console.log(verkiezing);
  if (gegevens.value == null) {
    gegevens.value = await leesCsv(verkiezing);
    ontbrekendeGemeenten.value = await leesOntbrekendeGemeentenCsv(verkiezing);
    console.log("ontbrekendeGemeenten", ontbrekendeGemeenten.value)
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
  <div class="midden" v-if="props.informatie.verkiezing == DEFAULT_VERKIEZING">
    <h3>Aantal gemeenten die gegevens hebben gepubliceerd</h3>
    <div style="margin-left: 10px" ref="ggGrafiek"></div>
    <h3 v-if="ontbrekendeGemeenten?.length !== 0">Ontbrekende gemeenten</h3>
    <table>
      <tr v-for="g in ontbrekendeGemeenten" :key="g"><td>{{ g }}</td></tr>
    </table>
    <p v-if="gegevens">De getoonde voortgang is vanaf ({{ new Intl.DateTimeFormat().format(gegevens[0].datum) }}). Vanaf dat moment zijn de gegevens via deze site bijgehouden.</p>
  </div>
  <div v-else class="midden"><h3>Voortgangsinformatie is alleen beschikbaar voor de {{  VERKIEZINGEN[DEFAULT_VERKIEZING]?.naam }} verkiezingen</h3></div>
</template>

<style scoped>
.midden {
  width: 100%;
  display: grid;
}

.midden > * {
  justify-self: center;
}

@media (max-width: 590px) {
  .midden > h3 {
    margin-left: 20px;
  }
}
.midden p {
  margin: 10px;
  margin-top: 20px;
}
</style>
