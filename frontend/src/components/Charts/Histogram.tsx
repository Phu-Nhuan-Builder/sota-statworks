"use client";
import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

export function Histogram({ data, title }: { data: number[]; title?: string }) {
  return (
    <Plot
      data={[{ type: "histogram", x: data, name: "Frequency" }]}
      layout={{
        title: title ? { text: title } : undefined,
        height: 300,
        margin: { t: 30, r: 20, b: 40, l: 50 },
        font: { family: "Arial", size: 9 },
      }}
      config={{ displayModeBar: false }}
    />
  );
}
