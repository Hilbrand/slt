export const PAGINA_IDS = ["eml", "gemeente", "kaart", "start", "tg", "voortgang"] as const;

export type PaginaID = (typeof PAGINA_IDS)[number];

export const VERKIEZING_IDS = ["ep2024", "tk2025", "gr2026"] as const;

export type VerkiezingID = (typeof VERKIEZING_IDS)[number];

export type VerkiezingType = {
  naam: string,
  datum: Date,
  aantalGemeenten: number,
};

export const VERKIEZINGEN: Record<VerkiezingID, VerkiezingType> = {
  //TK2023: "Tweede Kamer 2023",
  ep2024: {
    naam: "Europees Parlement 2024",
    datum: new Date(2024, 4, 6),
    aantalGemeenten: 345,
  },
  tk2025: {
    naam: "Tweede Kamer 2025",
    datum: new Date(2025, 9, 29),
    aantalGemeenten: 345,
  },
  gr2026: {
    naam: "Gemeenteraad 2026",
    datum: new Date(2026, 2, 18),
    aantalGemeenten: 345,
  }
};

export const TOEGANKELIJKHEDEN_IDS = [
  "lb",
  "ov",
  "to",
  "ho",
  "pd",
  "pa",
  "gi",
  "gu",
  "kb",
  "kg",
  "sa",
  "gt",
  "gs",
  "as",
  "nv",
] as const;

export type ToegankelijkhedenID = (typeof TOEGANKELIJKHEDEN_IDS)[number];

/**
 * Conversie map van key naar omschrijving toegankelijkheidscategorieen.
 */
export const TOEGANKELIJKHEDEN: Record<ToegankelijkhedenID, string> = {
  lb: "Toegankelijk voor mensen met een lichamelijke beperking",
  ov: "Toegankelijke ov-halte",
  to: "Toilet",
  ho: "Host",
  pd: "Prokkelduo",
  pa: "Prikkelarm",
  gi: "Geleidelijnen binnen",
  gu: "Geleidelijnen buiten",
  kb: "Kandidatenlijst in braille",
  kg: "Kandidatenlijst met grote letters",
  sa: "Stemmal met audio-ondersteuning",
  gt: "Gebarentolk (NGT)",
  gs: "Gebarentalig stembureaulid (NGT)",
  as: "Akoestiek geschikt voor slechthorenden",
  nv: "Niet verplichte toegankelijkheden",
};

export enum Visualisatie {
 TABEL = "TABEL",
 GRAFIEK = "GRAFIEK",
};

export const DEFAULT_PAGINA = "start" as PaginaID;
export const DEFAULT_VERKIEZING = "gr2026";
export const DEFAULT_GEMEENTE = "0518"; // Den Haag
export const DEFAULT_TOEGANKELIJKHEID = "lb";
export const DEFAULT_VISUALISATIE = Visualisatie.GRAFIEK;

export interface InformatieType {
  pagina: PaginaID;
  verkiezing: VerkiezingID;
  gemeente: string;
  toegankelijkheid: ToegankelijkhedenID;
  percentage: number;
  visualisatie: Visualisatie;
}

export type ToegankelijkheidDataType = {
  j? : number;
  ""?: number;
  n?: number;
  a?: number; // Op afstand aanwezige gebarentolk
  l?: number; // Lokaal aanwezige gebarentolk
  t?: number; // Toegankelijk toilet
  g?: number; // Genderneutraal toilet
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
  ja: string;
  nee: string;
  onbekend: string;
  geenGegevens: string;
  titel: boolean;
};

export const hoofdRegelToegankelijkheidCsv =
  ['Toegankelijkheid', 'Gebarentolk op locatie', 'Gebarentolk op afstand', 'Toegankelijk Toilet', 'Genderneutraal Toilet', 'Aanwezig', 'Onbekend', 'Afwezig'];

export const hoofdRegelGemeenteCsv =
  ['Gemeente', 'Gebarentolk op locatie', 'Gebarentolk op afstand', 'Toegankelijk Toilet', 'Genderneutraal Toilet', 'Aanwezig', 'Onbekend', 'Afwezig'];

export interface RegelDataCsv {
  (): string[][];
};
