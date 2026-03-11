"use client";
import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

export function ScatterPlot({
  x,
  y,
  xLabel,
  yLabel,
}: {
  x: number[];
  y: number[];
  xLabel?: string;
  yLabel?: string;
}) {
  return (
    <Plot
      data={[{ type: "scatter", mode: "markers", x, y }]}
      layout={{
        height: 300,
        xaxis: { title: xLabel },
        yaxis: { title: yLabel },
        margin: { t: 20, r: 20, b: 50, l: 50 },
        font: { family: "Arial", size: 9 },
      }}
      config={{ displayModeBar: false }}
    />
  );
}
