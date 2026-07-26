import type {
  ApiResponse,
  ClubListData,
  HealthData,
  StandingTableData,
} from "../types/api";

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

async function getApiData<T>(
  path: string,
  signal?: AbortSignal,
): Promise<ApiResponse<T>> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
    cache: "no-store",
    signal,
  });

  if (!response.ok) {
    throw new Error(`数据请求失败：HTTP ${response.status}`);
  }

  return (await response.json()) as ApiResponse<T>;
}

export function getClubs(
  signal?: AbortSignal,
): Promise<ApiResponse<ClubListData>> {
  return getApiData<ClubListData>("/clubs", signal);
}

export function getStandings(
  season = "2024-25",
  signal?: AbortSignal,
): Promise<ApiResponse<StandingTableData>> {
  return getApiData<StandingTableData>(
    `/standings?season=${encodeURIComponent(season)}`,
    signal,
  );
}
