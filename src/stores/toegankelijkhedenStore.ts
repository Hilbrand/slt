import { defineStore } from "pinia";
import type { GemeenteDataType, ToegankelijkheidType, ToegankelijkheidAreaType } from "@/types";

/**
 * Store voor toegankelijkheden per gemeente.
 */
export const useToegankelijkhedenStore = defineStore("toegankelijkheden", {
  state: () => ({
    resource_id: "",
    verkiezing: "",
    gemeenten: [],
    nationaal: ["", 0, {}] as ToegankelijkheidAreaType,
    atLeastOne: ["", 0, {}] as ToegankelijkheidAreaType,
    gemeenteData: {} as GemeenteDataType,
  }),

  actions: {
    async loadData(verkiezing: string) {
      try {
        const data = await fetch(verkiezing + "/stemlokalen.json");
        const json = await data.json();
        this.resource_id = json.resource_id;
        this.gemeenteData = json.data;
        this.nationaal = json.nationaal || ["", 0, {}];
        this.atLeastOne = json.atLeastOne || ["", 0, {}];
        const dataGemeenten = await fetch(verkiezing + "/gemeenten.json");
        this.gemeenten = await dataGemeenten.json();
        this.verkiezing = verkiezing;
      } catch (error) {
        console.error("Failed to load data:", error);
      }
    },
  },

  getters: {
    getAtLeastOne: (state) => (): ToegankelijkheidAreaType => state.atLeastOne,
    getNationaal: (state) => (): ToegankelijkheidAreaType => state.nationaal,
    getGemeenten: (state) => () => state.gemeenten,
    getGemeenteData: (state) => (): GemeenteDataType => state.gemeenteData,
    getGemeenteName:
      (state) =>
      (key: string | undefined): string =>
        state.gemeenteData
          ? (key === undefined || !(key in state.gemeenteData)
            ? (key === 'nationaal' ? "Alle stemlokalen" : "")
            : state.gemeenteData[key][0])
          : (state.gemeenten.filter(g => g[0] === key)[0][1]),
    getStemlokalen: (state) => (key: string | undefined) =>
      key !== undefined && state.gemeenteData && state.gemeenteData[key] ? state.gemeenteData[key][1] : 0,
    getResourceId: (state) => (): string => state.resource_id,
    getToegankelijkheden:
      (state) =>
      (key: string | undefined): ToegankelijkheidType =>
        key !== undefined && state.gemeenteData && state.gemeenteData[key] ? state.gemeenteData[key][2] : {},
    isDataForVerkiezing:
      (state) =>
      (verkiezing: string): boolean =>
        state.verkiezing === verkiezing,
    loadedVerkiezing: (state) => () => state.verkiezing,
  },
});
