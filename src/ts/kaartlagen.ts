import { Map, MapBrowserEvent, View } from "ol";
import type { FeatureLike } from "ol/Feature";
import { getTopLeft } from "ol/extent";
import { GeoJSON } from "ol/format";
import type BaseLayer from "ol/layer/Base";
import TileLayer from "ol/layer/Tile";
import VectorLayer from "ol/layer/Vector";
import type { Pixel } from "ol/pixel";
import { Projection } from "ol/proj";
import { WMTS } from "ol/source";
import VectorSource from "ol/source/Vector";
import { type StyleFunction } from "ol/style/Style";
import WMTSTileGrid from "ol/tilegrid/WMTS";

export type GeoLayer = VectorLayer<VectorSource>;

const extent = [-285401.92, 22598.08, 595401.9199999999, 903401.9199999999];
const resolutions = [
  3440.64, 1720.32, 860.16, 430.08, 215.04, 107.52, 53.76, 26.88, 13.44, 6.72, 3.36, 1.68, 0.84,
  0.42,
];
export const projection = new Projection({ code: "EPSG:28992", units: "m", extent: extent });
const matrixIds = Array.from<string>({ length: 26 });
for (let i = 0; i < 26; ++i) {
  matrixIds[i] = "EPSG:28992:" + i;
}

/**
 * Achtergrond kaartlaag
 */
export const achtergrondkaart = new TileLayer({
  source: new WMTS({
    url: "https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0?",
    layer: "grijs",
    matrixSet: "EPSG:28992",
    format: "image/png",
    projection: projection,
    tileGrid: new WMTSTileGrid({
      origin: getTopLeft(projection.getExtent()),
      resolutions: resolutions,
      matrixIds: matrixIds,
    }),
    style: "default",
    wrapX: true,
  }),
  opacity: 0.7,
});

export function maakGeoJsonKaartlaag(
  geojson: string,
  styleFunction: StyleFunction,
): VectorLayer<VectorSource> {
  return new VectorLayer({
    source: new VectorSource({
      url: geojson, // Path to your GeoJSON file
      format: new GeoJSON(),
    }),

    style: styleFunction,
  });
}

/**
 *
 * @param kaartlaag
 * @param herlaad
 */
export function updateKaartlaag(kaartlaag: GeoLayer | undefined, herlaad: boolean) {
  kaartlaag?.setVisible(true);
  if (herlaad) {
    kaartlaag?.getSource()?.changed();
  }
}

export function nieuweKaart(lagen: BaseLayer[]) {
  return new Map({
    target: "map", // The target HTML element id to render the map in
    layers: lagen,
    view: new View({
      projection: projection,
      center: [150000, 450000],
      minZoom: 2,
      zoom: 3,
    }),
  });
}

export type FeatureListener = (feature: FeatureLike) => void;

export class Kaart {
  map: Map;
  currentGemeente: string;
  currentFeature: FeatureLike | undefined;
  listeners: FeatureListener[];

  constructor(lagen: BaseLayer[]) {
    this.map = this.maakMap(lagen);
    this.currentGemeente = "";
    this.listeners = [];
  }

  addFeatureListener(listener: FeatureListener) {
    this.listeners.push(listener);
  }

  addLayer(layer: GeoLayer) {
    this.map.addLayer(layer);
  }

  getHover(): HTMLDivElement {
    return document.getElementById("hover") as HTMLDivElement;
  }

  displayFeatureInfo(pixel: Pixel, target: any) {
    const feature = target.closest(".ol-control")
      ? undefined
      : this.map.forEachFeatureAtPixel(pixel, function (feature) {
          return feature;
        });
    const info = this.getHover();

    if (feature) {
      this.listeners.forEach((l) => l(feature));
      if (window.innerWidth > 1024) {
        info.style.left = pixel[0] - (pixel[0] > (window.innerWidth - 600) ? 220 : 0) + "px";
      }else if (pixel[0] > window.innerWidth * 0.5) {
        info.style.left = "0px";
        info.style.right = "";
      } else {
        info.style.left = "";
        info.style.right = "10px";
      }
      if (pixel[1] + 350 > window.innerHeight) {
        info.style.top = pixel[1] - 220 + "px";
      } else {
        info.style.top = pixel[1] + "px";
      }
      if (feature !== this.currentFeature) {
        info.style.visibility = "visible";
      }
      this.currentFeature = feature;
    } else {
      this.currentFeature = undefined;
      info.style.visibility = "hidden";
    }
  }

  onClick(evt: MapBrowserEvent) {
    this.onPointMove(evt);
  }

  onPointMove(evt: MapBrowserEvent) {
    if (evt.dragging) {
      this.getHover().style.visibility = "hidden";
      this.currentFeature = undefined;
      return;
    }
    const pixel = this.map.getEventPixel(evt.originalEvent);
    if (pixel !== undefined) {
      this.displayFeatureInfo(pixel, evt.originalEvent.target);
    }
  }

  onPointerLeave(evt: Event) {
    this.currentFeature = undefined;
    this.getHover().style.visibility = "hidden";
  }

  maakMap(lagen: BaseLayer[]): Map {
    const map = nieuweKaart(lagen);

    map.on("click", (evt: MapBrowserEvent) => this.onClick(evt));
    map.on("pointermove", (evt) => this.onPointMove(evt));
    map.getTargetElement().addEventListener("pointerleave", (evt) => this.onPointerLeave(evt));
    return map;
  }
}

export default {
  achtergrondkaart,
  projection,
};
