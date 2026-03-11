import { create } from "zustand";
import type { DatasetMeta, OutputBlock } from "@/types/dataset";

interface FilterCondition {
  column: string;
  operator: "eq" | "ne" | "gt" | "lt" | "gte" | "lte" | "contains";
  value: string | number;
}

interface DatasetState {
  sessionId: string | null;
  metadata: DatasetMeta | null;
  activeFilters: FilterCondition[];
  outputBlocks: OutputBlock[];
  isLoading: boolean;
  error: string | null;

  // Actions
  setSession: (sessionId: string, meta: DatasetMeta) => void;
  setMetadata: (meta: DatasetMeta) => void;
  addOutputBlock: (block: OutputBlock) => void;
  removeOutputBlock: (id: string) => void;
  clearOutputBlocks: () => void;
  setActiveFilters: (filters: FilterCondition[]) => void;
  clearSession: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useDatasetStore = create<DatasetState>((set) => ({
  sessionId: null,
  metadata: null,
  activeFilters: [],
  outputBlocks: [],
  isLoading: false,
  error: null,

  setSession: (sessionId, meta) =>
    set({ sessionId, metadata: meta, error: null }),

  setMetadata: (meta) => set({ metadata: meta }),

  addOutputBlock: (block) =>
    set((state) => ({ outputBlocks: [block, ...state.outputBlocks] })),

  removeOutputBlock: (id) =>
    set((state) => ({
      outputBlocks: state.outputBlocks.filter((b) => b.id !== id),
    })),

  clearOutputBlocks: () => set({ outputBlocks: [] }),

  setActiveFilters: (filters) => set({ activeFilters: filters }),

  clearSession: () =>
    set({
      sessionId: null,
      metadata: null,
      activeFilters: [],
      outputBlocks: [],
      error: null,
    }),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),
}));
