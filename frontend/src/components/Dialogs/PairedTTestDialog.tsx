"use client";
import { useState } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { testsApi } from "@/lib/api";
import { toast } from "sonner";

interface Props { open: boolean; onClose: () => void; }

export function PairedTTestDialog({ open, onClose }: Props) {
  const { sessionId, metadata, addOutputBlock } = useDatasetStore();
  const [var1, setVar1] = useState("");
  const [var2, setVar2] = useState("");
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const numericVars = metadata?.variables.filter((v) => v.var_type === "numeric");

  const handleRun = async () => {
    if (!sessionId || !var1 || !var2) { toast.error("Select two variables"); return; }
    if (var1 === var2) { toast.error("Variables must differ"); return; }
    setLoading(true);
    try {
      const result = await testsApi.pairedTTest({ session_id: sessionId, var1, var2 });
      addOutputBlock({
        id: crypto.randomUUID(),
        type: "table",
        title: `Paired-Samples T Test — ${var1} vs ${var2}`,
        content: result,
        created_at: new Date(),
        procedure: "ttest-paired",
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
        <h3 className="font-bold text-sm mb-3">Paired-Samples T Test</h3>
        <div className="mb-2">
          <label className="text-xs text-gray-600 block mb-1">Variable 1:</label>
          <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={var1} onChange={(e) => setVar1(e.target.value)}>
            <option value="">-- Select --</option>
            {numericVars?.map((v) => <option key={v.name} value={v.name}>{v.name}</option>)}
          </select>
        </div>
        <div className="mb-4">
          <label className="text-xs text-gray-600 block mb-1">Variable 2:</label>
          <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={var2} onChange={(e) => setVar2(e.target.value)}>
            <option value="">-- Select --</option>
            {numericVars?.filter((v) => v.name !== var1).map((v) => <option key={v.name} value={v.name}>{v.name}</option>)}
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
