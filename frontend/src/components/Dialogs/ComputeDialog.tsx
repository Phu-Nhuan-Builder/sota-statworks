"use client";
import { useState } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { transformApi } from "@/lib/api";
import { toast } from "sonner";

interface Props { open: boolean; onClose: () => void; }

export function ComputeDialog({ open, onClose }: Props) {
  const { sessionId, metadata, setMetadata } = useDatasetStore();
  const [targetVar, setTargetVar] = useState("");
  const [expression, setExpression] = useState("");
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const insertVar = (varName: string) => setExpression((e) => e + varName);

  const handleRun = async () => {
    if (!sessionId || !targetVar || !expression.trim()) {
      toast.error("Enter target variable name and expression");
      return;
    }
    setLoading(true);
    try {
      const result = await transformApi.compute(sessionId, { target_var: targetVar, expression });
      if (result.meta) setMetadata(result.meta);
      toast.success(`Variable ${targetVar} computed`);
      onClose();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
      <div className="bg-white border border-gray-300 shadow-xl rounded w-[460px] p-4">
        <h3 className="font-bold text-sm mb-3">Compute Variable</h3>
        <div className="mb-2">
          <label className="text-xs text-gray-600 block mb-1">Target variable:</label>
          <input
            type="text"
            className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
            placeholder="new_variable_name"
            value={targetVar}
            onChange={(e) => setTargetVar(e.target.value)}
          />
        </div>
        <div className="mb-2">
          <label className="text-xs text-gray-600 block mb-1">Numeric expression:</label>
          <textarea
            className="w-full border border-gray-300 rounded px-2 py-1 text-sm font-mono h-16 resize-none"
            placeholder="e.g. var1 + var2 / 2"
            value={expression}
            onChange={(e) => setExpression(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label className="text-xs text-gray-600 block mb-1">Variables (click to insert):</label>
          <div className="flex flex-wrap gap-1 max-h-24 overflow-auto">
            {metadata?.variables.filter((v) => v.var_type === "numeric").map((v) => (
              <button
                key={v.name}
                onClick={() => insertVar(v.name)}
                className="text-xs px-2 py-0.5 border border-gray-300 rounded hover:bg-blue-50 hover:border-blue-300"
              >
                {v.name}
              </button>
            ))}
          </div>
        </div>
        <p className="text-[10px] text-gray-400 mb-3">
          Supported: +, -, *, /, (, ), abs(), sqrt(), log(), exp(), mean(), sum()
        </p>
        <div className="flex justify-end gap-2">
          <button onClick={onClose} className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50">Cancel</button>
          <button onClick={handleRun} disabled={loading} className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">{loading ? "Running..." : "OK"}</button>
        </div>
      </div>
    </div>
  );
}
