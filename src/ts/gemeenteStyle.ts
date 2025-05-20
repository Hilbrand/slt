import { type Ref } from "vue";
import { TOEGANKELIJKHEDEN_KEYS, type GemeenteDataType } from "@/ts/types";
import type { FeatureLike } from "ol/Feature";
import Fill from "ol/style/Fill";
import Stroke from "ol/style/Stroke";
import Style from "ol/style/Style";

export const color_unknown = "#F0E44244";

export function isAbove(data: GemeenteDataType, gem: string, tg: string, percentage: number) {
  if (!data || !gem) {
    return { total: 0, above: false };
  }
  const tgi = TOEGANKELIJKHEDEN_KEYS.indexOf(tg) || 0;
  const tgData = data[gem][2][tgi];
  const amount = tg == "gt" ? (tgData[1]?.a || 0) + (tgData[1]?.l || 0) : tgData[1]?.j || 0;
  const total = data[gem][1] ? data[gem][1] : 1;
  const above = Math.ceil((amount * 100) / total) >= percentage;
  return { total: total, above: above };
}

export function createGemeenteStyleFunction(
  data: Ref<GemeenteDataType>,
  tg: Ref<string>,
  percentage: Ref<number>,
) {
  return (feature: FeatureLike, resolution: number): Style => {
    const tgi = TOEGANKELIJKHEDEN_KEYS.indexOf(tg.value) || 0;
    const gem = feature.get("c");
    const { total, above } = isAbove(data.value, gem, tg.value, percentage.value);
    const color = above
      ? "#009E73"
      : gem.value && data.value[gem][2][tgi][1]?.n === total
        ? "#CC79A7"
        : color_unknown;

    return new Style({
      fill: new Fill({
        color: color,
      }),
      stroke: new Stroke({
        color: "#999",
        width: 0.4,
      }),
    });
  };
}
