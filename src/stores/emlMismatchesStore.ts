import { defineStore } from "pinia";

export const CODE = 0;
export const TOTAAL = 1;
export const ANDERE_NAAM = 2;
export const ANDERE_NAAM_PERCENTAGE = 3;
export const ANDERE_POSTCODE = 4;
export const ANDERE_POSTCODE_PERCENTAGE = 5;
export const ZELFDE = 6;
export const ZELFDE_PERCENTAGE = 7;

export type GemeenteMismatch = [string, number, number, number, number, number, number, number];

/**
 * Store voor data waarin aantal stemlokalen staan waarvan naam en/of postcode in
 * Kiesraad EML bestanden niet overeenkomt met gegevens uit WaarIsMijnStemlokaal.
 */
export const useEmlMismatchesStore = defineStore("emlMismatches", {
  state: () => ({
    verkiezing: "",
    mismatches: [] as GemeenteMismatch[],
  }),

  actions: {
    async loadData(verkiezing: string) {
      try {
        const data = await fetch(verkiezing + "_eml_mismatch.json");
        this.mismatches = await data.json();
        this.verkiezing = verkiezing;
        console.log(this.mismatches);
      } catch (error) {
        console.error("Failed to load data:", error);
      }
    },
  },

  getters: {
    getAll: (state) => (): GemeenteMismatch[] => state.mismatches,
    loadedVerkiezing: (state) => () => state.verkiezing,
  },
});
