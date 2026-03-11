"use client";
import { useState } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { descriptivesApi } from "@/lib/api";
import { toast } from "sonner";

interface Props { open: boolean; onClose: () => void; }

export function ExploreDialog({ open, onClose }: Props) {
  const { sessionId, metadata, addOutputBlock } = useDatasetStore();
  const [selected, setSelected] = useState("");
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const handleRun = async () => {
    if (!sessionId || !selected) { toast.error("Select a variable"); return; }
    setLoading(true);
    try {
      const result = await descriptivesApi.explore(sessionId, selected);
      addOutputBlock({
        id: crypto.randomUUID(),
        type: "table",
        title: `Explore — ${selected}`,
        content: result,
        created_at: new Date(),
        procedure: "explore",
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
      <div className="bg-white border border-gray-300 shadow-xl rounded w-80 p-4">
        <h3 className="font-bold text-sm mb-3">Explore</h3>
        <p className="text-xs text-gray-500 mb-3">Generates descriptive statistics, normality tests, and box plots.</p>
        <div className="mb-4">
          <label className="text-xs text-gray-600 block mb-1">Dependent variable:</label>
          <select
            className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
          >
            <option value="">-- Select --</option>
            {metadata?.variables
              .filter((v) => v.var_type === "numeric")
              .map((v) => <option key={v.name} value={v.name}>{v.name}{v.label ? ` — ${v.label}` : ""}</option>)}
          </select>
        </div>
        <div className="flex justify-end gap-2">
          <button onClick={onClose} className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50">Cancel</button>
          <button onClick={handleRun} disabled={loading} className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">{loading ? "Running..." : "OK"}</button>
        </div>
      </div>
    </div>
  );
}
