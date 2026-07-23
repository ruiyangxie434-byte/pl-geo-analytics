import type { ApiResponse, HealthData } from "../types/api";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api";

export async function getApiHealth(
  signal?: AbortSignal,
): Promise<ApiResponse<HealthData>> {
  const response = await fetch(`${API_BASE_URL}/health`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
    cache: "no-store",
    signal,
  });

  if (!response.ok) {
    throw new Error(`健康检查失败：HTTP ${response.status}`);
  }

  return (await response.json()) as ApiResponse<HealthData>;
}
