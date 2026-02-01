/**
 * Functies om download data samen te stellen.
 */
import { useToegankelijkhedenStore } from "@/stores/toegankelijkhedenStore";
import { TOEGANKELIJKHEDEN, type ToegankelijkhedenID, type ToegankelijkheidType } from "./types";

/**
 * Functie die data van ToegankelijkheidType omzet in array met toegankelijkheidsnaam en waarden.
 *
 * @param data ToegankelijkheidType data
 * @returns array van de data
 */
export function maakToegankelijkhedenData(data: ToegankelijkheidType): string[][] {
  return Object.entries(data).map(([tg, values]) => [
    TOEGANKELIJKHEDEN[tg as ToegankelijkhedenID],
    String(values.j ?? 0),
    String(values[""] ?? 0),
    String(values.n ?? 0),
  ]);
}

/**
 * Functie die voor alle gemeenten voor een specifieke toegankelijkheid de data in een array zet.
 * Eerste kolom is naam gemeente, rest van de kolommen zijn de waarden voor die gemeente.
 *
 * @param tg toegankelijkheid waarvoor de data moet worden omgezet
 * @returns array van de data van alle gemeenten
 */
export function maakGemeenteData(tg: ToegankelijkhedenID): string[][] {
  const toegankelijkhedenStore = useToegankelijkhedenStore();
  const gemeenten = toegankelijkhedenStore.getGemeenten();

  return gemeenten.map(gem => {
    const values = toegankelijkhedenStore.getToegankelijkheden(gem[0])[tg];
    return [
      gem[1],
      String(values.j ?? 0),
      String(values[""] ?? 0),
      String(values.n ?? 0),
    ];
  });
}
