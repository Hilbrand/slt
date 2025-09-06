<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { jsonToNavigatie } from "@/ts/navigatie";
import type { InformatieType, LegendaTextType, ToegankelijkheidType } from "@/ts/types";
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import Legenda from "@/components/LegendaComponent.vue";
import ToegankelijkheidsTable from "@/components/ToegankelijkheidsTable.vue";

const router = useRouter();

const props = defineProps<{
  informatie: InformatieType;
}>();

const toegankelijkhedenStore = useToegankelijkhedenStore();

const totaal = computed<number>(() =>
  toegankelijkhedenStore.loadedVerkiezing() == props.informatie?.verkiezing
    ? toegankelijkhedenStore.getStemlokalen(props.informatie?.gemeente)
    : 0,
);

const toegankelijkheden = computed<ToegankelijkheidType>(() =>
  toegankelijkhedenStore.loadedVerkiezing() == props.informatie?.verkiezing
    ? toegankelijkhedenStore.getToegankelijkheden(props.informatie?.gemeente)
    : {},
);

const gemeenten = computed(() =>
  toegankelijkhedenStore.loadedVerkiezing() == props.informatie?.verkiezing
    ? toegankelijkhedenStore.getGemeenten()
    : [],
);

function selected(gem: string): boolean {
  return props.informatie?.gemeente === gem;
}

function wisselGemeente(event: Event) {
  const e = event.target as HTMLInputElement;
  const copy = props.informatie;
  copy.gemeente = e.value;
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

<template v-if="toegankelijkheden !== undefined">
  <ToegankelijkheidsTable
    :totaal="totaal"
    :toegankelijkheden="toegankelijkheden">
    <tr>
      <td>
        <select class="select" @change="wisselGemeente">
          <option>Selecteer een gemeente</option>
          <option v-for="gem in gemeenten" :key="gem[0]"
              :value="gem[0]"
              :selected="selected(gem[0])">
            {{ gem[1] }}
          </option>
        </select>
      </td>
    </tr>
    <tr>
      <td>Aantal stemlokalen</td>
      <td class="row">
        <div class="cell yes" style="width: 100%">{{ totaal }}</div>
      </td>
    </tr>
  </ToegankelijkheidsTable>
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
