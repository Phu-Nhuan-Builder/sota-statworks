"use client";
import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

interface BoxPlotData {
  q1: number;
  median: number;
  q3: number;
  whisker_low: number;
  whisker_high: number;
  mild_outliers: number[];
  extreme_outliers: number[];
}

export function BoxPlot({ data, title }: { data: BoxPlotData; title?: string }) {
  return (
    <Plot
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      data={[{ type: "box", q1: [data.q1], median: [data.median], q3: [data.q3], lowerfence: [data.whisker_low], upperfence: [data.whisker_high], name: title || "Box Plot" } as any]}
      layout={{
        title: title ? { text: title } : undefined,
        height: 300,
        margin: { t: 30, r: 20, b: 30, l: 40 },
        font: { family: "Arial", size: 9 },
      }}
      config={{ displayModeBar: false }}
    />
  );
}
