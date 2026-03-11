"use client";

import { useState } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { filesApi } from "@/lib/api";
import { toast } from "sonner";
import type { VariableMeta, VariableMeasure, VariableType, VariableRole } from "@/types/dataset";

const MEASURE_OPTIONS: VariableMeasure[] = ["nominal", "ordinal", "scale"];
const TYPE_OPTIONS: VariableType[] = ["numeric", "string", "date"];
const ROLE_OPTIONS: VariableRole[] = ["input", "target", "both", "none", "partition", "split"];

export function VariableView() {
  const { sessionId, metadata, setMetadata } = useDatasetStore();
  const [saving, setSaving] = useState<string | null>(null);

  if (!sessionId || !metadata) {
    return (
      <div className="flex items-center justify-center h-full text-gray-400 text-sm">
        No dataset loaded
      </div>
    );
  }

  const handleCellChange = async (
    varName: string,
    field: keyof VariableMeta,
    value: string | number
  ) => {
    const updatedVars = metadata.variables.map((v) =>
      v.name === varName ? { ...v, [field]: value } : v
    );
    const updatedMeta = { ...metadata, variables: updatedVars };
    setMetadata(updatedMeta);

    setSaving(varName);
    try {
      await filesApi.updateMeta(sessionId, updatedMeta);
    } catch (err) {
      toast.error("Failed to save variable metadata");
    } finally {
      setSaving(null);
    }
  };

  const columns: { key: keyof VariableMeta; label: string; width: string; type?: "text" | "number" | "select"; options?: string[] }[] = [
    { key: "name", label: "Name", width: "w-28", type: "text" },
    { key: "var_type", label: "Type", width: "w-24", type: "select", options: TYPE_OPTIONS },
    { key: "width", label: "Width", width: "w-16", type: "number" },
    { key: "decimals", label: "Decimals", width: "w-20", type: "number" },
    { key: "label", label: "Label", width: "w-48", type: "text" },
    { key: "measure", label: "Measure", width: "w-24", type: "select", options: MEASURE_OPTIONS },
    { key: "role", label: "Role", width: "w-24", type: "select", options: ROLE_OPTIONS },
  ];

  return (
    <div className="overflow-auto h-full bg-white">
      <table className="spss-table min-w-full">
        <thead className="sticky top-0 z-10">
          <tr>
            <th className="w-12 text-center">#</th>
            {columns.map((col) => (
              <th key={col.key} className={`${col.width} text-left`}>
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {metadata.variables.map((v, idx) => (
            <tr key={v.name} className="hover:bg-blue-50 transition-colors">
              <td className="text-center text-gray-500 bg-spss-gray">{idx + 1}</td>
              {columns.map((col) => (
                <td key={col.key} className="p-0">
                  {col.type === "select" ? (
                    <select
                      className="w-full h-full px-1 py-0.5 text-xs bg-transparent border-0 focus:outline-none focus:bg-yellow-50"
                      value={String(v[col.key])}
                      onChange={(e) => handleCellChange(v.name, col.key, e.target.value)}
                    >
                      {col.options?.map((opt) => (
                        <option key={opt} value={opt}>{opt}</option>
                      ))}
                    </select>
                  ) : (
                    <input
                      type={col.type === "number" ? "number" : "text"}
                      className="w-full h-full px-1 py-0.5 text-xs bg-transparent border-0 focus:outline-none focus:bg-yellow-50"
                      value={String(v[col.key] ?? "")}
                      onChange={(e) =>
                        handleCellChange(
                          v.name,
                          col.key,
                          col.type === "number" ? Number(e.target.value) : e.target.value
                        )
                      }
                    />
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {saving && (
        <div className="fixed bottom-4 right-4 bg-blue-600 text-white text-xs px-3 py-1.5 rounded shadow">
          Saving…
        </div>
      )}
    </div>
  );
}
