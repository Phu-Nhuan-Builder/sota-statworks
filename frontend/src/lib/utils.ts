import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatNumber(value: number | null | undefined, decimals = 3): string {
  if (value === null || value === undefined || isNaN(value)) return ".";
  return value.toFixed(decimals);
}

export function formatPValue(p: number | null | undefined): string {
  if (p === null || p === undefined) return ".";
  if (p < 0.001) return "< .001";
  return p.toFixed(3);
}

export function significanceStars(p: number): string {
  if (p < 0.001) return "***";
  if (p < 0.01) return "**";
  if (p < 0.05) return "*";
  return "";
}
