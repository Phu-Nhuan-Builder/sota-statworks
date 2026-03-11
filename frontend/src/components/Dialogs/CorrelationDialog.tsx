"use client";
import { useState } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { regressionApi } from "@/lib/api";
import { toast } from "sonner";

interface Props { open: boolean; onClose: () => void; }

export function CorrelationDialog({ open, onClose }: Props) {
  const { sessionId, metadata, addOutputBlock } = useDatasetStore();
  const [selectedVars, setSelectedVars] = useState<string[]>([]);
  const [method, setMethod] = useState("pearson");
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const toggleVar = (name: string) => setSelectedVars((prev) =>
    prev.includes(name) ? prev.filter((v) => v !== name) : [...prev, name]
  );

  const handleRun = async () => {
    if (!sessionId || selectedVars.length < 2) { toast.error("Select at least 2 variables"); return; }
    setLoading(true);
    try {
      const result = await regressionApi.correlation({ session_id: sessionId, variables: selectedVars, method });
      addOutputBlock({
        id: crypto.randomUUID(),
        type: "table",
        title: `${method === "pearson" ? "Pearson" : "Spearman"} Correlations`,
        content: result,
        created_at: new Date(),
        procedure: "correlation",
      });
      onClose();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
      <div className="bg-white border border-gray-300 shadow-xl rounded w-96 p-4">
        <h3 className="font-bold text-sm mb-3">Bivariate Correlations</h3>
        <div className="mb-2">
          <label className="text-xs text-gray-600 block mb-1">Correlation coefficient:</label>
          <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={method} onChange={(e) => setMethod(e.target.value)}>
            <option value="pearson">Pearson</option>
            <option value="spearman">Spearman</option>
          </select>
        </div>
        <div className="mb-3">
          <label className="text-xs text-gray-600 block mb-1">Variables:</label>
          <div className="border border-gray-300 rounded h-40 overflow-auto p-1">
            {metadata?.variables.filter((v) => v.var_type === "numeric").map((v) => (
              <label key={v.name} className="flex items-center gap-2 px-1 py-0.5 hover:bg-gray-50 cursor-pointer text-sm">
                <input type="checkbox" checked={selectedVars.includes(v.name)} onChange={() => toggleVar(v.name)} />
                <span>{v.name}{v.label ? ` — ${v.label}` : ""}</span>
              </label>
            ))}
          </div>
        </div>
        <div className="flex justify-end gap-2">
          <button onClick={onClose} className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50">Cancel</button>
          <button onClick={handleRun} disabled={loading} className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">{loading ? "Running..." : "OK"}</button>
        </div>
      </div>
    </div>
  );
}
