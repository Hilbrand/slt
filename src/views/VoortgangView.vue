<script setup lang="ts">
import { DEFAULT_VERKIEZING, type InformatieType, type VerkiezingID } from "@/ts/types";
import { leesCsv, maakGrafiek, type GemeentenGepubliceerdItem } from "@/ts/voortgangGrafiek";
import { onMounted, onUnmounted, ref, watch } from "vue";

const props = defineProps<{
  informatie: InformatieType;
}>();

const ggGrafiek = ref(null);
const ingelezenVerkiezing = ref<VerkiezingID>(DEFAULT_VERKIEZING);
const gegevens = ref<GemeentenGepubliceerdItem[] | null>(null);
const nietDeelnemendeGemeenten = ref<string[] | null>(null);
const ontbrekendeGemeenten = ref<string[] | null>(null);

async function leesGemeentenCsv(csv: string): Promise<string[]> {
    try {
      const data = await fetch(csv);
    const gemeenten = await data.text();

    if (gemeenten.includes('html')) {
      return [];
    }
    return gemeenten == "" ? [] : gemeenten.split('\n');
    } catch(error) {
      console.log(`"Fout bij laden ${csv} gemeenten:"`, error);
      return [];
    }
}

async function leesNietDeelnemendeGemeentenCsv(verkiezing: string): Promise<string[]> {
  return leesGemeentenCsv(verkiezing + "/niet-deelnemende-gemeenten.csv");
}

async function leesOntbrekendeGemeentenCsv(verkiezing: string): Promise<string[]> {
  return leesGemeentenCsv(verkiezing + "/ontbrekende_gemeenten.csv");
}

async function tekenGrafiek() {
  if (gegevens.value == null || ingelezenVerkiezing.value != props.informatie.verkiezing && props.informatie.verkiezing != null) {
    ingelezenVerkiezing.value = props.informatie.verkiezing;
    gegevens.value = await leesCsv(ingelezenVerkiezing.value);
    nietDeelnemendeGemeenten.value = await leesNietDeelnemendeGemeentenCsv(ingelezenVerkiezing.value);
    ontbrekendeGemeenten.value = await leesOntbrekendeGemeentenCsv(ingelezenVerkiezing.value);
  }
  if (ggGrafiek.value !== null && gegevens.value != null) {
    maakGrafiek(ingelezenVerkiezing.value, gegevens.value, ggGrafiek.value, window.innerWidth);
  }
}

watch(
  () => props.informatie,
  (newState) => {
    if (newState) {
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
  <div class="midden" v-if="props.informatie.verkiezing != 'ep2024'">
    <h3>Aantal gemeenten die gegevens hebben gepubliceerd</h3>
    <div style="margin-left: 10px" ref="ggGrafiek"></div>
    <h3 v-if="ontbrekendeGemeenten?.length !== 0">Ontbrekende gemeenten ({{ (ontbrekendeGemeenten?.length || 1) - 1 }})</h3>
    <table>
      <tr v-for="g in ontbrekendeGemeenten" :key="g"><td>{{ g }}</td></tr>
    </table>
    <h3 v-if="nietDeelnemendeGemeenten?.length !== 0">Gemeenten die niet zelf de gegevens hebben aangeleverd ({{ (nietDeelnemendeGemeenten?.length || 1) - 1 }})</h3>
    <table>
      <tr v-for="g in nietDeelnemendeGemeenten" :key="g"><td>{{ g }}</td></tr>
    </table>
    <p v-if="gegevens">De getoonde voortgang is vanaf ({{ new Intl.DateTimeFormat().format(gegevens[0]?.datum) }}). Vanaf dat moment zijn de gegevens via deze site bijgehouden.</p>
  </div>
  <div v-else class="midden"><h3>Voortgangsinformatie was nog niet op deze site beschikbaar voor deze verkiezingen.</h3></div>
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
