import type {
  AgentAnalysisData,
  AgentAnalysisRequest,
  AgentCapabilitiesData,
  AgentPlayerOptionData,
  ApiResponse,
  ClubDetailData,
  ClubListData,
  HealthData,
  PlayerLabData,
  PlayerLabItem,
  PlayerLabQuery,
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

export function getClub(
  slug: string,
  signal?: AbortSignal,
): Promise<ApiResponse<ClubDetailData>> {
  return getApiData<ClubDetailData>(
    `/clubs/${encodeURIComponent(slug)}`,
    signal,
  );
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

export function getPlayers(
  options: PlayerLabQuery = {},
  signal?: AbortSignal,
): Promise<ApiResponse<PlayerLabData>> {
  const search = new URLSearchParams({
    season: options.season ?? "2024-25",
    minimum_minutes: String(options.minimumMinutes ?? 450),
    sort_by: options.sortBy ?? "goals_per90",
    order: options.order ?? "desc",
    limit: String(options.limit ?? 100),
    offset: String(options.offset ?? 0),
  });
  if (options.query) {
    search.set("query", options.query);
  }
  if (options.position) {
    search.set("position", options.position);
  }
  if (options.clubSlug) {
    search.set("club_slug", options.clubSlug);
  }
  return getApiData<PlayerLabData>(`/players?${search.toString()}`, signal);
}

export function getPlayer(
  slug: string,
  season = "2024-25",
  signal?: AbortSignal,
): Promise<ApiResponse<PlayerLabItem>> {
  return getApiData<PlayerLabItem>(
    `/players/${encodeURIComponent(slug)}?season=${encodeURIComponent(season)}`,
    signal,
  );
}

export function getAgentPlayers(
  season = "2024-25",
  signal?: AbortSignal,
): Promise<ApiResponse<AgentPlayerOptionData>> {
  return getApiData<AgentPlayerOptionData>(
    `/agent/players?season=${encodeURIComponent(season)}`,
    signal,
  );
}

export function getAgentCapabilities(
  signal?: AbortSignal,
): Promise<ApiResponse<AgentCapabilitiesData>> {
  return getApiData<AgentCapabilitiesData>(
    "/agent/capabilities",
    signal,
  );
}

export async function runAgentAnalysis(
  payload: AgentAnalysisRequest,
  signal?: AbortSignal,
): Promise<ApiResponse<AgentAnalysisData>> {
  const response = await fetch(`${API_BASE_URL}/agent/analyze`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
    cache: "no-store",
    signal,
  });

  const body = (await response.json()) as ApiResponse<AgentAnalysisData>;
  if (!response.ok) {
    throw new Error(body.message || `Agent 请求失败：HTTP ${response.status}`);
  }
  return body;
}
