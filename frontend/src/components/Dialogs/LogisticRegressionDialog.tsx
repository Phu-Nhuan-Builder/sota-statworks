"use client";
import { useState } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { regressionApi } from "@/lib/api";
import { toast } from "sonner";

interface Props { open: boolean; onClose: () => void; }

export function LogisticRegressionDialog({ open, onClose }: Props) {
  const { sessionId, metadata, addOutputBlock } = useDatasetStore();
  const [dependent, setDependent] = useState("");
  const [independents, setIndependents] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const toggleIV = (name: string) => setIndependents((prev) =>
    prev.includes(name) ? prev.filter((v) => v !== name) : [...prev, name]
  );

  const handleRun = async () => {
    if (!sessionId || !dependent || independents.length === 0) { toast.error("Select variables"); return; }
    setLoading(true);
    try {
      const result = await regressionApi.logisticBinary({ session_id: sessionId, dependent, independents });
      addOutputBlock({
        id: crypto.randomUUID(),
        type: "table",
        title: "Binary Logistic Regression",
        subtitle: `DV: ${dependent}`,
        content: result,
        created_at: new Date(),
        procedure: "logistic",
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
        <h3 className="font-bold text-sm mb-3">Binary Logistic Regression</h3>
        <div className="mb-2">
          <label className="text-xs text-gray-600 block mb-1">Dependent variable (binary):</label>
          <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={dependent} onChange={(e) => setDependent(e.target.value)}>
            <option value="">-- Select --</option>
            {metadata?.variables.map((v) => <option key={v.name} value={v.name}>{v.name}</option>)}
          </select>
        </div>
        <div className="mb-3">
          <label className="text-xs text-gray-600 block mb-1">Covariates:</label>
          <div className="border border-gray-300 rounded h-36 overflow-auto p-1">
            {metadata?.variables.filter((v) => v.var_type === "numeric" && v.name !== dependent).map((v) => (
              <label key={v.name} className="flex items-center gap-2 px-1 py-0.5 hover:bg-gray-50 cursor-pointer text-sm">
                <input type="checkbox" checked={independents.includes(v.name)} onChange={() => toggleIV(v.name)} />
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
