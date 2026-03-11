"use client";
import { useState } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { factorApi } from "@/lib/api";
import { toast } from "sonner";

interface Props { open: boolean; onClose: () => void; }

export function FactorAnalysisDialog({ open, onClose }: Props) {
  const { sessionId, metadata, addOutputBlock } = useDatasetStore();
  const [selectedVars, setSelectedVars] = useState<string[]>([]);
  const [nFactors, setNFactors] = useState(3);
  const [extraction, setExtraction] = useState("principal");
  const [rotation, setRotation] = useState("varimax");
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const toggleVar = (name: string) => setSelectedVars((prev) =>
    prev.includes(name) ? prev.filter((v) => v !== name) : [...prev, name]
  );

  const handleRun = async () => {
    if (!sessionId || selectedVars.length < 2) { toast.error("Select at least 2 variables"); return; }
    setLoading(true);
    try {
      const result = await factorApi.efa({ session_id: sessionId, variables: selectedVars, n_factors: nFactors, extraction, rotation });
      if (result.job_id) {
        toast.info("Factor analysis queued — check output when complete");
      } else {
        addOutputBlock({
          id: crypto.randomUUID(),
          type: "table",
          title: "Factor Analysis (EFA)",
          content: result,
          created_at: new Date(),
          procedure: "efa",
        });
      }
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
        <h3 className="font-bold text-sm mb-3">Factor Analysis (EFA)</h3>
        <div className="grid grid-cols-2 gap-2 mb-2">
          <div>
            <label className="text-xs text-gray-600 block mb-1">Extraction:</label>
            <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={extraction} onChange={(e) => setExtraction(e.target.value)}>
              <option value="principal">Principal Axis</option>
              <option value="minres">MinRes</option>
              <option value="ml">ML</option>
            </select>
          </div>
          <div>
            <label className="text-xs text-gray-600 block mb-1">Rotation:</label>
            <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={rotation} onChange={(e) => setRotation(e.target.value)}>
              <option value="varimax">Varimax</option>
              <option value="oblimin">Oblimin</option>
              <option value="quartimax">Quartimax</option>
              <option value="promax">Promax</option>
            </select>
          </div>
        </div>
        <div className="mb-2">
          <label className="text-xs text-gray-600 block mb-1">Number of factors:</label>
          <input
            type="number"
            min="1"
            max="20"
            className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
            value={nFactors}
            onChange={(e) => setNFactors(parseInt(e.target.value))}
          />
        </div>
        <div className="mb-3">
          <label className="text-xs text-gray-600 block mb-1">Variables:</label>
          <div className="border border-gray-300 rounded h-36 overflow-auto p-1">
            {metadata?.variables.filter((v) => v.var_type === "numeric").map((v) => (
              <label key={v.name} className="flex items-center gap-2 px-1 py-0.5 hover:bg-gray-50 cursor-pointer text-sm">
                <input type="checkbox" checked={selectedVars.includes(v.name)} onChange={() => toggleVar(v.name)} />
                <span>{v.name}</span>
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
