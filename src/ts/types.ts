export const PAGINA_IDS = ["eml", "gemeente", "kaart", "start"] as const;

export type PaginaID = (typeof PAGINA_IDS)[number];

export const VERKIEZING_IDS = ["ep2024"] as const;

export type VerkiezingID = (typeof VERKIEZING_IDS)[number];

export const VERKIEZINGEN: Record<VerkiezingID, string> = {
  //TK2023: "Tweede Kamer 2023",
  ep2024: "Europees Parlement 2024",
};

export const TOEGANKELIJKHEDEN_IDS = [
  "lb",
  "ov",
  "to",
  "ho",
  "pa",
  "gi",
  "gu",
  "kb",
  "kg",
  "sa",
  "gt",
  "gs",
  "as",
] as const;

export type ToegankelijkhedenID = (typeof TOEGANKELIJKHEDEN_IDS)[number];

/**
 * Conversie map van key naar omschrijving toegankelijkheidscategorieen.
 */
export const TOEGANKELIJKHEDEN: Record<ToegankelijkhedenID, string> = {
  lb: "Toegankelijk voor mensen met een lichamelijke beperking",
  ov: "Toegankelijke ov-halte",
  to: "Gehandicaptentoilet",
  ho: "Host",
  pa: "Prikkelarm",
  gi: "Geleidelijnen binnen",
  gu: "Geleidelijnen buiten",
  kb: "Kandidatenlijst in braille",
  kg: "Kandidatenlijst met grote letters",
  sa: "Stemmal met audio-ondersteuning",
  gt: "Gebarentolk (NGT)",
  gs: "Gebarentalig stembureaulid (NGT)",
  as: "Akoestiek geschikt voor slechthorenden",
};

export const DEFAULT_PAGINA = "start" as PaginaID;
export const DEFAULT_VERKIEZING = "ep2024";
export const DEFAULT_GEMEENTE = "0518"; // Den Haag
export const DEFAULT_TOEGANKELIJKHEID = "lb";

export interface InformatieType {
  pagina: PaginaID;
  verkiezing: VerkiezingID;
  gemeente: string;
  toegankelijkheid: ToegankelijkhedenID;
  percentage: number;
}

export type ToegankelijkheidDataType = {
  j? : number;
  ""?: number;
  n?: number;
  a?: number;
  l?: number;
};

export type ToegankelijkheidDataTypeKey = keyof ToegankelijkheidDataType;

export type ToegankelijkheidType = { [tg:string]: ToegankelijkheidDataType };
export type ToegankelijkheidAreaType = [string, number, ToegankelijkheidType];

export type GemeenteDataType = {
  [gmcode: string]: ToegankelijkheidAreaType;
};

export type ToegankelijkhedenDataType = {
  resource_id: string;
  data: GemeenteDataType;
};

export type LegendaTextType = {
  no: string;
  nodata: string;
  yes: string;
  title: boolean;
};
