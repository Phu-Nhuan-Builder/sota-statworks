"use client";
import { useState } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { transformApi } from "@/lib/api";
import { toast } from "sonner";

interface Props { open: boolean; onClose: () => void; }

interface SortKey {
  variable: string;
  order: "asc" | "desc";
}

export function SortDialog({ open, onClose }: Props) {
  const { sessionId, metadata } = useDatasetStore();
  const [sortKeys, setSortKeys] = useState<SortKey[]>([{ variable: "", order: "asc" }]);
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const addKey = () => setSortKeys((k) => [...k, { variable: "", order: "asc" }]);
  const removeKey = (i: number) => setSortKeys((k) => k.filter((_, idx) => idx !== i));
  const updateKey = (i: number, field: keyof SortKey, value: string) =>
    setSortKeys((k) => k.map((key, idx) => (idx === i ? { ...key, [field]: value } : key)));

  const handleRun = async () => {
    if (!sessionId) return;
    const validKeys = sortKeys.filter((k) => k.variable);
    if (validKeys.length === 0) { toast.error("Select at least one sort variable"); return; }
    setLoading(true);
    try {
      await transformApi.sort(sessionId, { sort_keys: validKeys });
      toast.success("Cases sorted");
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
        <h3 className="font-bold text-sm mb-3">Sort Cases</h3>
        <div className="mb-3 space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs text-gray-600">Sort by:</label>
            <button onClick={addKey} className="text-xs text-blue-600 hover:text-blue-800">+ Add key</button>
          </div>
          {sortKeys.map((key, i) => (
            <div key={i} className="flex items-center gap-2">
              <select
                className="flex-1 border border-gray-300 rounded px-2 py-1 text-xs"
                value={key.variable}
                onChange={(e) => updateKey(i, "variable", e.target.value)}
              >
                <option value="">-- Select --</option>
                {metadata?.variables.map((v) => <option key={v.name} value={v.name}>{v.name}</option>)}
              </select>
              <select
                className="w-20 border border-gray-300 rounded px-2 py-1 text-xs"
                value={key.order}
                onChange={(e) => updateKey(i, "order", e.target.value)}
              >
                <option value="asc">Asc</option>
                <option value="desc">Desc</option>
              </select>
              {sortKeys.length > 1 && (
                <button onClick={() => removeKey(i)} className="text-red-400 hover:text-red-600 text-xs">✕</button>
              )}
            </div>
          ))}
        </div>
        <div className="flex justify-end gap-2">
          <button onClick={onClose} className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50">Cancel</button>
          <button onClick={handleRun} disabled={loading} className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">{loading ? "Sorting..." : "OK"}</button>
        </div>
      </div>
    </div>
  );
}
