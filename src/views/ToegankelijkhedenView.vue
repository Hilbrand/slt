<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { jsonToNavigatie } from "@/ts/navigatie";
import { TOEGANKELIJKHEDEN, TOEGANKELIJKHEDEN_IDS, type InformatieType, type LegendaTextType, type ToegankelijkhedenID, type ToegankelijkheidAreaType, type ToegankelijkheidType } from "@/ts/types";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import Legenda from "@/components/LegendaComponent.vue";
import ToegankelijkheidsTable from "@/components/ToegankelijkheidsTable.vue";
import ToegankelijkheidRegel from "@/components/ToegankelijkheidRegel.vue";

const router = useRouter();

const props = defineProps<{
  informatie: InformatieType;
}>();

const toegankelijkhedenStore = useToegankelijkhedenStore();

// const toegankelijkheid = ref<ToegankelijkhedenID>("lb");
const toegankelijkheidText = computed<string>(() =>
  props.informatie?.toegankelijkheid && TOEGANKELIJKHEDEN[props.informatie?.toegankelijkheid] || "",
);

const nationaal = computed<ToegankelijkheidAreaType>(() =>
  toegankelijkhedenStore.loadedVerkiezing() == props.informatie?.verkiezing
    ? toegankelijkhedenStore.getNational()
    : ["", 0, {}],
);

const gemeenten = computed(() =>
  toegankelijkhedenStore.isDataForVerkiezing(props.informatie?.verkiezing)
    ? toegankelijkhedenStore.getGemeenten()
    : [],
);

function selected(tg: string): boolean {
  return props.informatie?.toegankelijkheid === tg;
}

function wisselToegankelijkheid(event: Event) {
  const e = event.target as HTMLInputElement;
  const copy = props.informatie;
  copy.toegankelijkheid = e.value as ToegankelijkhedenID;
  router.replace({ query: jsonToNavigatie(copy) });
}

const legendaText = {
  ja: "Aantal stemlokalen waar de toegankelijkheid aanwezig is",
  nee: "Aantal stemlokalen waar de toegankelijkheid afwezig is",
  onbekend: "Aantal stemlokalen waar de toegankelijkheidsinformatie onbekend is",
  geenGegevens: "",
  titel: true,
} as LegendaTextType;
</script>

<template>
  <table class="grid">
    <tbody>
      <tr>
        <td>
          <select class="select" @change="wisselToegankelijkheid">
            <option v-for="row in TOEGANKELIJKHEDEN_IDS" :key="row"
                :value="row"
                :selected="selected(row)">
              {{ TOEGANKELIJKHEDEN[row] }}
            </option>
          </select>
        </td>
      </tr>
      <ToegankelijkheidRegel
        naam="Alle stemlokalen"
        :toegankelijkheid="toegankelijkheidText"
        :tid="props.informatie.toegankelijkheid"
        :totaal="nationaal[1]"
        groep="gemeenten"
        :toegankelijkheden="nationaal[2]"/>
      <ToegankelijkheidRegel
        v-for="gem in gemeenten"
        :key="gem[0]"
        :naam="gem[1]"
        :toegankelijkheid="toegankelijkheidText"
        :tid="props.informatie.toegankelijkheid"
        :totaal="toegankelijkhedenStore.getStemlokalen(gem[0])"
        groep="gemeenten"
        :toegankelijkheden="toegankelijkhedenStore.getToegankelijkheden(gem[0])"/>
    </tbody>
  </table>
  <Legenda :legendaText="legendaText" />
</template>

<style scoped>
.select {
  width: 100%;
  line-height: 30px;
  height: 30px;
  background-color: var(--color-selectiebox);
  border-radius: 5px;
}
</style>
