import type { InformatieType } from "@/ts/types";
import {
  DEFAULT_GEMEENTE,
  DEFAULT_PAGINA,
  DEFAULT_TOEGANKELIJKHEID,
  DEFAULT_VERKIEZING,
  DEFAULT_VISUALISATIE,
} from "@/ts/types";
import type { LocationQuery, LocationQueryRaw } from "vue-router";

export function navigatieToJson(query: LocationQuery): InformatieType {
  return {
    pagina: query.page || DEFAULT_PAGINA,
    verkiezing: query.v || DEFAULT_VERKIEZING,
    gemeente: query.g || DEFAULT_GEMEENTE,
    toegankelijkheid: query.t || DEFAULT_TOEGANKELIJKHEID,
    percentage: query.p || 1,
    visualisatie: query.vis || DEFAULT_VISUALISATIE,
  } as InformatieType;
}

export function jsonToNavigatie(info: InformatieType): LocationQueryRaw {
  return {
    page: info.pagina,
    v: info.verkiezing,
    g: info.gemeente,
    t: info.toegankelijkheid,
    p: info.percentage,
    vis: info.visualisatie,
  } as LocationQueryRaw;
}

export default {
  navigatieToJson,
  jsonToNavigatie,
};
