"use client";
import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

export function ScreePlot({ eigenvalues }: { eigenvalues: number[] }) {
  const x = eigenvalues.map((_, i) => i + 1);
  return (
    <Plot
      data={[
        {
          type: "scatter",
          mode: "lines+markers",
          x,
          y: eigenvalues,
          name: "Eigenvalue",
        },
        {
          type: "scatter",
          mode: "lines",
          x: [1, x.length],
          y: [1, 1],
          name: "Eigenvalue = 1",
          line: { dash: "dash", color: "red" },
        },
      ]}
      layout={{
        title: { text: "Scree Plot" },
        height: 300,
        xaxis: { title: { text: "Factor Number" } },
        yaxis: { title: { text: "Eigenvalue" } },
        margin: { t: 30, r: 20, b: 50, l: 50 },
        font: { family: "Arial", size: 9 },
      }}
      config={{ displayModeBar: false }}
    />
  );
}
