"use client";
import { useState } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { regressionApi } from "@/lib/api";
import { toast } from "sonner";

interface Props { open: boolean; onClose: () => void; }

export function LinearRegressionDialog({ open, onClose }: Props) {
  const { sessionId, metadata, addOutputBlock } = useDatasetStore();
  const [dependent, setDependent] = useState("");
  const [independents, setIndependents] = useState<string[]>([]);
  const [method, setMethod] = useState("enter");
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const toggleIV = (name: string) => setIndependents((prev) =>
    prev.includes(name) ? prev.filter((v) => v !== name) : [...prev, name]
  );

  const handleRun = async () => {
    if (!sessionId || !dependent || independents.length === 0) {
      toast.error("Select dependent and independent variables");
      return;
    }
    setLoading(true);
    try {
      const result = await regressionApi.linear({ session_id: sessionId, dependent, independents, method });
      addOutputBlock({
        id: crypto.randomUUID(),
        type: "table",
        title: "Linear Regression",
        subtitle: `DV: ${dependent}`,
        content: result,
        created_at: new Date(),
        procedure: "linear_regression",
      });
      onClose();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Error");
    } finally {
      setLoading(false);
    }
  };

  const numVars = metadata?.variables.filter((v) => v.var_type === "numeric");

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
      <div className="bg-white border border-gray-300 shadow-xl rounded w-96 p-4">
        <h3 className="font-bold text-sm mb-3">Linear Regression</h3>
        <div className="mb-2">
          <label className="text-xs text-gray-600 block mb-1">Dependent variable:</label>
          <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={dependent} onChange={(e) => setDependent(e.target.value)}>
            <option value="">-- Select --</option>
            {numVars?.map((v) => <option key={v.name} value={v.name}>{v.name}</option>)}
          </select>
        </div>
        <div className="mb-2">
          <label className="text-xs text-gray-600 block mb-1">Method:</label>
          <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={method} onChange={(e) => setMethod(e.target.value)}>
            <option value="enter">Enter</option>
            <option value="stepwise">Stepwise</option>
            <option value="forward">Forward</option>
            <option value="backward">Backward</option>
          </select>
        </div>
        <div className="mb-3">
          <label className="text-xs text-gray-600 block mb-1">Independent variables:</label>
          <div className="border border-gray-300 rounded h-36 overflow-auto p-1">
            {numVars?.filter((v) => v.name !== dependent).map((v) => (
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
