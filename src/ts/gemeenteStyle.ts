import { type Ref } from "vue";
import { GEEN_VERKIEZING, type GemeenteDataType, type ToegankelijkhedenID } from "@/ts/types";
import type { FeatureLike } from "ol/Feature";
import Fill from "ol/style/Fill";
import Stroke from "ol/style/Stroke";
import Style from "ol/style/Style";

export const color_onbekend = "#f0e442";
const color_ja = "#009e73";
const color_nee = "#cc79a7";
const color_geen_gegevens = "#7774";
const kleur_geen_verkiezing = "#fff";

export function isBovenPercentage(data: GemeenteDataType, gem: string, tg: ToegankelijkhedenID | undefined, percentage: number) {
  if (!data || !gem || !tg) {
    return { total: 0, above: false };
  }
  const tgData = data[gem] && data[gem][2] && data[gem][2][tg];
  const amount = tgData?.j || 0;
  const totaal = data[gem] && data[gem][1] ? data[gem][1] : 1;
  const bovenPercentage = Math.ceil((amount * 100) / totaal) >= percentage;
  return { totaal: totaal, bovenPercentage: bovenPercentage };
}

export function createGemeenteStyleFunction(
  data: Ref<GemeenteDataType>,
  tg: Ref<ToegankelijkhedenID>,
  percentage: Ref<number>,
) {
  return (feature: FeatureLike, _resolution: number): Style => {
    const gem = feature.get("c");
    const { total, bovenPercentage } = isBovenPercentage(data.value, gem, tg.value, percentage.value);
    let kleur: string;

    if (bovenPercentage) {
      kleur = color_ja;
    } else if (data.value[gem]) {
      // @ts-expect-error Bij gemeenten waar geen verkiezingen wordt gehouden staat in kolom 1 de waarde 'geen verkiezing' ipv een getal
      if (data.value[gem][1] === GEEN_VERKIEZING) {
        kleur = kleur_geen_verkiezing;
      } else {
        kleur = data.value[gem][2]
            ? (data.value[gem][2][tg.value]?.n === total ? color_nee : color_onbekend)
            : color_geen_gegevens;
      }
    } else {
      kleur = color_geen_gegevens;
    }
    return new Style({
      fill: new Fill({
        color: kleur,
      }),
      stroke: new Stroke({
        color: "#333",
        width: 0.6,
      }),
    });
  };
}
