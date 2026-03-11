"use client";

import { useDatasetStore } from "@/stores/datasetStore";
import { OutputBlock } from "./OutputBlock";
import { FileText } from "lucide-react";

export function OutputViewer() {
  const { outputBlocks, clearOutputBlocks } = useDatasetStore();

  if (outputBlocks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-gray-400 gap-3">
        <FileText className="w-12 h-12 text-gray-300" />
        <p className="text-sm">No output yet</p>
        <p className="text-xs text-gray-300">Run a statistical procedure from the Analyze menu</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Toolbar */}
      <div className="flex items-center justify-between border-b border-gray-200 bg-gray-50 px-4 py-2">
        <span className="text-xs text-gray-500">{outputBlocks.length} output block{outputBlocks.length !== 1 ? "s" : ""}</span>
        <button
          onClick={clearOutputBlocks}
          className="text-xs text-red-500 hover:text-red-700 transition-colors"
        >
          Clear All
        </button>
      </div>

      {/* Output blocks */}
      <div className="flex-1 overflow-auto p-6 space-y-6 bg-gray-50">
        {outputBlocks.map((block) => (
          <OutputBlock key={block.id} block={block} />
        ))}
      </div>
    </div>
  );
}
