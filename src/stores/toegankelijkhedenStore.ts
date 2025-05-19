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
    national: ["", 0, []] as ToegankelijkheidAreaType,
    atLeastOne: ["", 0, []] as ToegankelijkheidAreaType,
    gemeenteData: {} as GemeenteDataType,
  }),

  actions: {
    async loadData(verkiezing: string) {
      try {
        const data = await fetch(verkiezing + ".json");
        const json = await data.json();
        this.resource_id = json.resource_id;
        this.gemeenteData = json.data;
        this.national = json.national;
        this.atLeastOne = json.atLeastOne;
        const dataGemeenten = await fetch(verkiezing + "_gemeenten.json");
        const jsonGemeenten = await dataGemeenten.json();
        this.gemeenten = jsonGemeenten;
        this.verkiezing = verkiezing;
      } catch (error) {
        console.error("Failed to load data:", error);
      }
    },
  },

  getters: {
    getAtLeastOne: (state) => (): ToegankelijkheidAreaType => state.atLeastOne,
    getNational: (state) => (): ToegankelijkheidAreaType => state.national,
    getGemeenten: (state) => () => state.gemeenten,
    getGemeenteData: (state) => (): GemeenteDataType => state.gemeenteData,
    getGemeenteName:
      (state) =>
      (key: string | undefined): string =>
        key === undefined || !(key in state.gemeenteData) ? "" : state.gemeenteData[key][0],
    getStemlokalen: (state) => (key: string | undefined) =>
      key == undefined ? 0 : state.gemeenteData[key][1],
    getResourceId: (state) => (): string => state.resource_id,
    getToegankelijkheden:
      (state) =>
      (key: string | undefined): ToegankelijkheidType[] =>
        key == undefined ? [] : state.gemeenteData[key][2],
    isDataForVerkiezing:
      (state) =>
      (verkiezing: string): boolean =>
        state.verkiezing === verkiezing,

    loadedVerkiezing: (state) => () => state.verkiezing,
  },
});
