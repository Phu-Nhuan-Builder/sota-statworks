"use client";
import { useState } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { testsApi } from "@/lib/api";
import { toast } from "sonner";

interface Props { open: boolean; onClose: () => void; }

export function IndependentTTestDialog({ open, onClose }: Props) {
  const { sessionId, metadata, addOutputBlock } = useDatasetStore();
  const [testVar, setTestVar] = useState("");
  const [groupVar, setGroupVar] = useState("");
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const numericVars = metadata?.variables.filter((v) => v.var_type === "numeric");
  const catVars = metadata?.variables.filter((v) => v.measure !== "scale");

  const handleRun = async () => {
    if (!sessionId || !testVar || !groupVar) { toast.error("Select test and grouping variables"); return; }
    setLoading(true);
    try {
      const result = await testsApi.independentTTest({ session_id: sessionId, test_var: testVar, group_var: groupVar });
      addOutputBlock({
        id: crypto.randomUUID(),
        type: "table",
        title: `Independent Samples T-Test — ${testVar}`,
        content: result,
        created_at: new Date(),
        procedure: "ttest-independent",
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
        <h3 className="font-bold text-sm mb-3">Independent-Samples T Test</h3>
        <div className="mb-2">
          <label className="text-xs text-gray-600 block mb-1">Test variable (numeric):</label>
          <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={testVar} onChange={(e) => setTestVar(e.target.value)}>
            <option value="">-- Select --</option>
            {numericVars?.map((v) => <option key={v.name} value={v.name}>{v.name}</option>)}
          </select>
        </div>
        <div className="mb-4">
          <label className="text-xs text-gray-600 block mb-1">Grouping variable (2 groups):</label>
          <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={groupVar} onChange={(e) => setGroupVar(e.target.value)}>
            <option value="">-- Select --</option>
            {catVars?.filter((v) => v.name !== testVar).map((v) => <option key={v.name} value={v.name}>{v.name}</option>)}
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
