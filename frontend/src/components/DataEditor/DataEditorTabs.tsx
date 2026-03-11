"use client";

import { useState } from "react";
import { DataView } from "./DataView";
import { VariableView } from "./VariableView";

type Tab = "data" | "variable";

export function DataEditorTabs() {
  const [activeTab, setActiveTab] = useState<Tab>("data");

  return (
    <div className="flex flex-col h-full">
      {/* Content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === "data" ? <DataView /> : <VariableView />}
      </div>

      {/* Bottom Tab Bar (SPSS-style) */}
      <div className="flex border-t border-gray-400 bg-gray-200 px-2 pt-1 gap-1">
        <button
          onClick={() => setActiveTab("data")}
          className={`px-6 py-1 text-xs rounded-t border border-b-0 transition-colors ${
            activeTab === "data"
              ? "bg-white border-gray-400 font-semibold"
              : "bg-gray-300 border-gray-300 hover:bg-gray-100"
          }`}
        >
          Data View
        </button>
        <button
          onClick={() => setActiveTab("variable")}
          className={`px-6 py-1 text-xs rounded-t border border-b-0 transition-colors ${
            activeTab === "variable"
              ? "bg-white border-gray-400 font-semibold"
              : "bg-gray-300 border-gray-300 hover:bg-gray-100"
          }`}
        >
          Variable View
        </button>
      </div>
    </div>
  );
}
