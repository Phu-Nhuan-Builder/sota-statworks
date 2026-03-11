"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useDatasetStore } from "@/stores/datasetStore";
import { filesApi } from "@/lib/api";
import type { DataPage } from "@/types/dataset";
import { formatNumber } from "@/lib/utils";
import { Loader2 } from "lucide-react";

const PAGE_SIZE = 100;

export function DataView() {
  const { sessionId, metadata } = useDatasetStore();
  const [dataPage, setDataPage] = useState<DataPage | null>(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const fetchData = useCallback(async (p: number) => {
    if (!sessionId) return;
    setLoading(true);
    try {
      const result = await filesApi.getData(sessionId, p, PAGE_SIZE);
      setDataPage(result);
    } catch (err) {
      console.error("Failed to fetch data", err);
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  useEffect(() => {
    fetchData(page);
  }, [page, fetchData]);

  if (!sessionId || !metadata) {
    return (
      <div className="flex items-center justify-center h-full text-gray-400 text-sm">
        No dataset loaded
      </div>
    );
  }

  const totalPages = dataPage ? Math.ceil(dataPage.total / PAGE_SIZE) : 1;
  const variables = metadata.variables;
  const rows = dataPage?.data ?? [];

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Table */}
      <div ref={containerRef} className="flex-1 overflow-auto">
        <table className="spss-table min-w-full">
          <thead className="sticky top-0 z-10">
            <tr>
              {/* Row number header */}
              <th className="spss-table-rn sticky left-0 z-20 bg-spss-table-header min-w-[48px] text-center">
                #
              </th>
              {variables.map((v) => (
                <th key={v.name} className="whitespace-nowrap">
                  {v.name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={variables.length + 1} className="text-center py-8">
                  <Loader2 className="inline w-5 h-5 animate-spin text-gray-400" />
                </td>
              </tr>
            ) : rows.length === 0 ? (
              <tr>
                <td colSpan={variables.length + 1} className="text-center py-8 text-gray-400">
                  No data
                </td>
              </tr>
            ) : (
              rows.map((row, rowIdx) => {
                const globalIdx = (page - 1) * PAGE_SIZE + rowIdx + 1;
                return (
                  <tr key={rowIdx} className="hover:bg-blue-50 transition-colors">
                    <td className="text-center text-gray-500 bg-spss-gray border-r border-spss-table-border sticky left-0">
                      {globalIdx}
                    </td>
                    {variables.map((v) => {
                      const raw = row[v.name];
                      const hasLabel = v.value_labels && raw !== null && raw !== undefined && String(raw) in v.value_labels;
                      const display = hasLabel
                        ? v.value_labels[String(raw)]
                        : raw === null || raw === undefined
                        ? "."
                        : v.var_type === "numeric" && typeof raw === "number"
                        ? formatNumber(raw, v.decimals)
                        : String(raw);
                      return (
                        <td key={v.name} className={v.var_type === "string" ? "text-left" : ""}>
                          {display}
                        </td>
                      );
                    })}
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {dataPage && totalPages > 1 && (
        <div className="flex items-center justify-between border-t border-gray-200 bg-gray-50 px-4 py-2">
          <span className="text-xs text-gray-500">
            Showing {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, dataPage.total)} of {dataPage.total} cases
          </span>
          <div className="flex gap-1">
            <button
              onClick={() => setPage(1)}
              disabled={page === 1}
              className="px-2 py-1 text-xs border border-gray-300 rounded disabled:opacity-40 hover:bg-gray-100"
            >
              «
            </button>
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-2 py-1 text-xs border border-gray-300 rounded disabled:opacity-40 hover:bg-gray-100"
            >
              ‹
            </button>
            <span className="px-3 py-1 text-xs border border-gray-300 rounded bg-white">
              {page} / {totalPages}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="px-2 py-1 text-xs border border-gray-300 rounded disabled:opacity-40 hover:bg-gray-100"
            >
              ›
            </button>
            <button
              onClick={() => setPage(totalPages)}
              disabled={page === totalPages}
              className="px-2 py-1 text-xs border border-gray-300 rounded disabled:opacity-40 hover:bg-gray-100"
            >
              »
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
