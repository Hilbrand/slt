import { type Ref } from "vue";
import { type GemeenteDataType, type ToegankelijkhedenID } from "@/ts/types";
import type { FeatureLike } from "ol/Feature";
import Fill from "ol/style/Fill";
import Stroke from "ol/style/Stroke";
import Style from "ol/style/Style";

export const color_onbekend = "#f0e442";
const color_ja = "#009e73";
const color_nee = "#cc79a7";
const color_geen_gegevens = "#7774";


export function isAbove(data: GemeenteDataType, gem: string, tg: ToegankelijkhedenID | undefined, percentage: number) {
  if (!data || !gem || !tg) {
    return { total: 0, above: false };
  }
  const tgData = data[gem] && data[gem][2] && data[gem][2][tg];
  const amount = tgData?.j || 0;
  const total = data[gem] && data[gem][1] ? data[gem][1] : 1;
  const above = Math.ceil((amount * 100) / total) >= percentage;
  return { total: total, above: above };
}

export function createGemeenteStyleFunction(
  data: Ref<GemeenteDataType>,
  tg: Ref<ToegankelijkhedenID>,
  percentage: Ref<number>,
) {
  return (feature: FeatureLike, _resolution: number): Style => {
    const gem = feature.get("c");
    const { total, above } = isAbove(data.value, gem, tg.value, percentage.value);
    const color = above
      ? color_ja
      : (data.value[gem]
        ? (data.value[gem][2][tg.value]?.n === total ? color_nee : color_onbekend)
        : color_geen_gegevens);
    return new Style({
      fill: new Fill({
        color: color,
      }),
      stroke: new Stroke({
        color: "#333",
        width: 0.6,
      }),
    });
  };
}
