import { defineStore } from "pinia";
import { GeoJSON } from "ol/format";

type DataMap = { [key: string]: string };

/**
 * Store voor gemeenten om gemeente te koppelen aan wijk.
 */
export const useGemeentenStore = defineStore("gemeenten", {
  state: () => ({
    dataMap: {} as DataMap,
  }),

  actions: {
    async loadData() {
      try {
        const data = await fetch("gemeenten.geojson");
        const json = await data.json();
        const geojson = new GeoJSON().readFeatures(json);
        geojson.forEach((f) => (this.dataMap[f.getProperties()["c"]] = f.getProperties()["n"]));
      } catch (error) {
        console.error("Failed to load data:", error);
      }
    },
  },

  getters: {
    getGemeente: (state) => (key: string | undefined) =>
      key == undefined ? "" : state.dataMap[key],
  },
});
