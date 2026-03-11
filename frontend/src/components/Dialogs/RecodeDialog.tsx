"use client";
import { useState } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { transformApi } from "@/lib/api";
import { toast } from "sonner";

interface Props { open: boolean; onClose: () => void; }

interface RecodeRule {
  from: string;
  to: string;
}

export function RecodeDialog({ open, onClose }: Props) {
  const { sessionId, metadata, setMetadata } = useDatasetStore();
  const [sourceVar, setSourceVar] = useState("");
  const [targetVar, setTargetVar] = useState("");
  const [rules, setRules] = useState<RecodeRule[]>([{ from: "", to: "" }]);
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const addRule = () => setRules((r) => [...r, { from: "", to: "" }]);
  const removeRule = (i: number) => setRules((r) => r.filter((_, idx) => idx !== i));
  const updateRule = (i: number, field: "from" | "to", value: string) =>
    setRules((r) => r.map((rule, idx) => (idx === i ? { ...rule, [field]: value } : rule)));

  const handleRun = async () => {
    if (!sessionId || !sourceVar || !targetVar) { toast.error("Select source variable and enter target name"); return; }
    if (rules.some((r) => !r.from || !r.to)) { toast.error("All recode rules must be filled in"); return; }
    setLoading(true);
    try {
      const result = await transformApi.recode(sessionId, {
        source_var: sourceVar,
        target_var: targetVar,
        rules: rules.map((r) => ({ from: r.from, to: r.to })),
      });
      if (result.meta) setMetadata(result.meta);
      toast.success(`Variable ${targetVar} created`);
      onClose();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
      <div className="bg-white border border-gray-300 shadow-xl rounded w-[420px] p-4">
        <h3 className="font-bold text-sm mb-3">Recode into Different Variables</h3>
        <div className="grid grid-cols-2 gap-2 mb-3">
          <div>
            <label className="text-xs text-gray-600 block mb-1">Source variable:</label>
            <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm" value={sourceVar} onChange={(e) => setSourceVar(e.target.value)}>
              <option value="">-- Select --</option>
              {metadata?.variables.map((v) => <option key={v.name} value={v.name}>{v.name}</option>)}
            </select>
          </div>
          <div>
            <label className="text-xs text-gray-600 block mb-1">Target variable name:</label>
            <input
              type="text"
              className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
              placeholder="new_var"
              value={targetVar}
              onChange={(e) => setTargetVar(e.target.value)}
            />
          </div>
        </div>

        <div className="mb-3">
          <div className="flex items-center justify-between mb-1">
            <label className="text-xs text-gray-600">Recode rules (Old → New):</label>
            <button onClick={addRule} className="text-xs text-blue-600 hover:text-blue-800">+ Add rule</button>
          </div>
          <div className="space-y-1 max-h-40 overflow-auto">
            {rules.map((rule, i) => (
              <div key={i} className="flex items-center gap-2">
                <input
                  type="text"
                  placeholder="Old value"
                  className="flex-1 border border-gray-300 rounded px-2 py-1 text-xs"
                  value={rule.from}
                  onChange={(e) => updateRule(i, "from", e.target.value)}
                />
                <span className="text-gray-400 text-xs">→</span>
                <input
                  type="text"
                  placeholder="New value"
                  className="flex-1 border border-gray-300 rounded px-2 py-1 text-xs"
                  value={rule.to}
                  onChange={(e) => updateRule(i, "to", e.target.value)}
                />
                <button onClick={() => removeRule(i)} className="text-red-400 hover:text-red-600 text-xs">✕</button>
              </div>
            ))}
          </div>
          <p className="text-[10px] text-gray-400 mt-1">Use &quot;ELSE&quot; as old value to catch all remaining values.</p>
        </div>

        <div className="flex justify-end gap-2">
          <button onClick={onClose} className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50">Cancel</button>
          <button onClick={handleRun} disabled={loading} className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">{loading ? "Running..." : "OK"}</button>
        </div>
      </div>
    </div>
  );
}
