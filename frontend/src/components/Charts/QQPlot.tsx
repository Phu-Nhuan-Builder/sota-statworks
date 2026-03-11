"use client";
import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

export function QQPlot({
  observed,
  theoretical,
  fitSlope,
  fitIntercept,
}: {
  observed: number[];
  theoretical: number[];
  fitSlope: number;
  fitIntercept: number;
}) {
  const lineX = [Math.min(...theoretical), Math.max(...theoretical)];
  const lineY = lineX.map((x) => fitSlope * x + fitIntercept);

  return (
    <Plot
      data={[
        {
          type: "scatter",
          mode: "markers",
          x: theoretical,
          y: observed,
          name: "Observed",
        },
        {
          type: "scatter",
          mode: "lines",
          x: lineX,
          y: lineY,
          name: "Expected",
          line: { color: "red" },
        },
      ]}
      layout={{
        title: "Normal Q-Q Plot",
        height: 300,
        xaxis: { title: "Theoretical Quantiles" },
        yaxis: { title: "Observed Values" },
        margin: { t: 30, r: 20, b: 50, l: 50 },
        font: { family: "Arial", size: 9 },
      }}
      config={{ displayModeBar: false }}
    />
  );
}
