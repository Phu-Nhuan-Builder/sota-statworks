"use client";
import { useState } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { descriptivesApi } from "@/lib/api";
import { toast } from "sonner";

interface Props { open: boolean; onClose: () => void; }

export function CrosstabsDialog({ open, onClose }: Props) {
  const { sessionId, metadata, addOutputBlock } = useDatasetStore();
  const [rowVar, setRowVar] = useState("");
  const [colVar, setColVar] = useState("");
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const handleRun = async () => {
    if (!sessionId || !rowVar || !colVar) { toast.error("Select both row and column variables"); return; }
    if (rowVar === colVar) { toast.error("Row and column variables must differ"); return; }
    setLoading(true);
    try {
      const result = await descriptivesApi.crosstabs(sessionId, rowVar, colVar);
      addOutputBlock({
        id: crypto.randomUUID(),
        type: "table",
        title: `Crosstabulation: ${rowVar} × ${colVar}`,
        content: result,
        created_at: new Date(),
        procedure: "crosstabs",
      });
      onClose();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Error");
    } finally {
      setLoading(false);
    }
  };

  const catVars = metadata?.variables.filter((v) => v.measure !== "scale");

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
      <div className="bg-white border border-gray-300 shadow-xl rounded w-80 p-4">
        <h3 className="font-bold text-sm mb-3">Crosstabs</h3>
        <div className="mb-2">
          <label className="text-xs text-gray-600 block mb-1">Row variable:</label>
          <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={rowVar} onChange={(e) => setRowVar(e.target.value)}>
            <option value="">-- Select --</option>
            {catVars?.map((v) => <option key={v.name} value={v.name}>{v.name}</option>)}
          </select>
        </div>
        <div className="mb-4">
          <label className="text-xs text-gray-600 block mb-1">Column variable:</label>
          <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={colVar} onChange={(e) => setColVar(e.target.value)}>
            <option value="">-- Select --</option>
            {catVars?.filter((v) => v.name !== rowVar).map((v) => <option key={v.name} value={v.name}>{v.name}</option>)}
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
