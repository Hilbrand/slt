import * as d3 from "d3";
import { VERKIEZINGEN, type VerkiezingID } from "./types";

export type GemeentenGepubliceerdItem = {
  datum: Date,
  aantal: number
}

const parseDatum = d3.timeParse("%d-%m-%Y");

export async function leesCsv(verkiezing: string): Promise<GemeentenGepubliceerdItem[]> {
  return await d3.csv(verkiezing + "_voortgang.csv", (d: { datum: any; aantal: string; }) => {
    return {
      datum: parseDatum(d.datum),
      aantal: parseInt(d.aantal),
    } as GemeentenGepubliceerdItem
  });
}

export async function maakGrafiek(verkiezingCode: VerkiezingID, data: GemeentenGepubliceerdItem[], element: string, innerWidth: number) {
  const verkiezing = VERKIEZINGEN[verkiezingCode]
  const marginWidth = 30;
  const marginHeight = 10;
  const width = Math.min(innerWidth - marginWidth - marginWidth, 1000);
  const height = Math.min(width - 50, 500);

  const x = d3.scaleTime()
    .domain([data[0].datum, verkiezing.datum])
    .range([0, width - marginWidth])
  const y = d3.scaleLinear()
    .domain([0, 400])
    .range([height - marginHeight, 0])

  d3.select(element).selectChild().remove();

  const svg = d3.select(element)
    .append("svg")
    .attr("class", "voortgang")
    .attr("width", width + marginWidth)
    .attr("height", height + marginHeight)
    .attr('transform', `translate(0,${marginHeight})`);

  // X-AS
  const xAs = d3.axisBottom(x)

  svg.append("g")
    .attr("transform", `translate(${marginWidth},${height - marginHeight})`)
    .call(xAs);

  svg.append("g")
    .attr("class", "as")
    .attr("transform", `translate(${marginWidth}, ${height - marginHeight})`)
    // @ts-expect-error 2e argument is optioneel
    .call(xAs
      .tickSize(-height)
      .ticks(d3.timeSunday)
      // @ts-expect-error "" is legaal
      .tickFormat("")
    )

  // Maak verticale lijnen wat vager
  svg.selectAll('.as .tick line').attr('opacity', 0.4)

  // Y-AS
  const yAs = d3.axisLeft(y)

  svg.append("g")
    .attr("transform", `translate(${marginWidth},0)`)
    .call(yAs
      .tickValues([0, 50, 100, 150, 200, 250, 300, verkiezing.aantalGemeenten])
    );

  svg
    .append("g")
    .append("line")
    .attr("class", "totaal-lijn")
    .attr("transform", `translate(${marginWidth},0)`)
    .attr("x1", x(data[0].datum))
    .attr("x2", x(verkiezing.datum))
    .attr("y1", y(verkiezing.aantalGemeenten))
    .attr("y2", y(verkiezing.aantalGemeenten));

  const laatste = data[data.length - 1];
  svg
    .append("text")
    .text(laatste.aantal)
    .attr("class", "tekst")
    .attr("x", x(laatste.datum) + 40)
    .attr("y", y(laatste.aantal) + 5)

  // Grafiek
  const lijn = d3.line()
    // @ts-expect-error typescript ziet alleen nummer array
    .x(d => x(d.datum))
    // @ts-expect-error typescript ziet alleen nummer array
    .y(d => y(d.aantal));

  const tooltip = d3.select("body")
    .append("div")
    .style("position", "absolute");

  svg.append("path")
    .attr("class", "lijn")
    .attr("transform", `translate(${marginWidth},0)`)
    .datum(data)
    // @ts-expect-error lijn is specifiek type en dat mag
    .attr("d", lijn)
    .on("mousemove", function(event) {
      const [xp, _yp] = d3.pointer(event);
      const xValue = x.invert(xp);
      const bisect = d3.bisector((d: GemeentenGepubliceerdItem) => d.datum).left;
      const index = bisect(data, xValue);
      const aantal = data[index]?.aantal;

      tooltip.style("opacity", 1)
        .html(`${aantal || ''}`)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 0) + "px");
    })
    .on("mouseout", () => tooltip.style("opacity", 0));
}
