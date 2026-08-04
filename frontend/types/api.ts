export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T | null;
}

export interface HealthData {
  service: string;
  status: "healthy";
  environment: string;
  version: string;
}

export interface StadiumData {
  name: string;
  latitude: number;
  longitude: number;
}

export interface ClubSummary {
  id: number;
  name: string;
  short_name: string;
  slug: string;
  city: string;
  stadium: StadiumData;
  founded_year: number | null;
  primary_color: string;
  source_kind: "reference" | "sample";
}

export interface ClubListData {
  items: ClubSummary[];
  total: number;
  player_total: number;
  limit: number;
  offset: number;
  season: string;
  is_complete: boolean;
  source_name: string;
  source_url: string;
  sample_notice: string;
}

export interface ClubPlayerSummary {
  id: number;
  full_name: string;
  slug: string;
  shirt_number: number | null;
  position: string;
  nationality: string;
  date_of_birth: string | null;
  source_kind: "sample";
}

export interface ClubDetailData extends ClubSummary {
  players: ClubPlayerSummary[];
}

export interface StandingClub {
  id: number;
  name: string;
  short_name: string;
  slug: string;
  primary_color: string;
}

export interface StandingItem {
  position: number;
  club: StandingClub;
  played: number;
  won: number;
  drawn: number;
  lost: number;
  goals_for: number;
  goals_against: number;
  goal_difference: number;
  points: number;
  source_kind: "historical" | "sample";
}

export interface StandingTableData {
  season: string;
  items: StandingItem[];
  total: number;
  is_partial: boolean;
  snapshot_date: string;
  source_name: string;
  source_url: string;
  sample_notice: string;
}

export type PlayerPosition = "FWD" | "MID" | "DEF" | "GK";

export type PlayerSortKey =
  | "full_name"
  | "club"
  | "position"
  | "minutes"
  | "goals"
  | "assists"
  | "goals_per90"
  | "assists_per90"
  | "shots_per90"
  | "key_passes_per90"
  | "tackles_per90"
  | "interceptions_per90"
  | "expected_goals_per90";

export type PlayerSortOrder = "asc" | "desc";

export interface PlayerClubData {
  name: string;
  short_name: string;
  slug: string;
  primary_color: string;
}

export interface PlayerSeasonTotals {
  appearances: number;
  starts: number;
  minutes: number;
  goals: number;
  assists: number;
  shots: number;
  key_passes: number;
  tackles: number;
  interceptions: number;
  expected_goals: number | null;
}

export interface PlayerPer90Metrics {
  goals_per90: number;
  assists_per90: number;
  shots_per90: number;
  key_passes_per90: number;
  tackles_per90: number;
  interceptions_per90: number;
  expected_goals_per90: number;
}

export interface PlayerMetricPercentiles {
  goals_per90: number;
  assists_per90: number;
  shots_per90: number;
  key_passes_per90: number;
  tackles_per90: number;
  interceptions_per90: number;
  expected_goals_per90: number;
}

export interface PlayerPercentileProfile {
  scope: "position_sample" | "all_sample_players";
  peer_count: number;
  metrics: PlayerMetricPercentiles;
}

export interface PlayerLabItem {
  id: number;
  full_name: string;
  slug: string;
  shirt_number: number | null;
  position: PlayerPosition;
  nationality: string;
  date_of_birth: string | null;
  source_kind: "sample";
  club: PlayerClubData;
  season: string;
  totals: PlayerSeasonTotals;
  per90: PlayerPer90Metrics;
  percentiles: PlayerPercentileProfile;
}

export interface PlayerLabData {
  items: PlayerLabItem[];
  total: number;
  pool_total: number;
  season: string;
  minimum_minutes: number;
  limit: number;
  offset: number;
  sort_by: PlayerSortKey;
  order: PlayerSortOrder;
  available_positions: PlayerPosition[];
  available_clubs: PlayerClubData[];
  sample_notice: string;
  percentile_notice: string;
}

export interface PlayerLabQuery {
  season?: string;
  minimumMinutes?: number;
  query?: string;
  position?: PlayerPosition;
  clubSlug?: string;
  sortBy?: PlayerSortKey;
  order?: PlayerSortOrder;
  limit?: number;
  offset?: number;
}

export type AgentFocus =
  | "balanced"
  | "scoring"
  | "creativity"
  | "pressing";

export type AgentRequestedFocus = AgentFocus | "auto";

export interface AgentPlayerOption {
  slug: string;
  full_name: string;
  club_name: string;
  club_color: string;
  position: string;
  minutes: number;
}

export interface AgentPlayerOptionData {
  items: AgentPlayerOption[];
  total: number;
  season: string;
  sample_notice: string;
}

export interface AgentPlayerProfile extends AgentPlayerOption {
  nationality: string;
}

export interface AgentMetricValue {
  player_slug: string;
  value: number;
  percentile: number;
}

export interface AgentMetricComparison {
  key: string;
  label: string;
  unit: string;
  weight: number;
  values: AgentMetricValue[];
  leader_slug: string | null;
}

export interface AgentStep {
  index: number;
  title: string;
  tool: string;
  detail: string;
  status: "completed";
}

export interface AgentEvidence {
  title: string;
  detail: string;
  leader_slug: string | null;
}

export interface AgentRecommendation {
  winner_slug: string;
  headline: string;
  summary: string;
  confidence: number;
  scores: Record<string, number>;
}

export interface AgentGeneration {
  mode: "local_rules" | "qwen_enhanced";
  status: "completed" | "not_configured" | "fallback" | "pending";
  provider: "local" | "qwen";
  model: string | null;
  note: string;
}

export interface AgentCapabilitiesData {
  qwen_configured: boolean;
  provider: "qwen";
  model: string;
  default_mode: "local_rules" | "qwen_enhanced";
  message: string;
}

export interface AgentAnalysisData {
  run_id: string;
  task_type: "player_comparison";
  question: string;
  season: string;
  requested_focus: AgentRequestedFocus;
  focus: AgentFocus;
  focus_label: string;
  players: AgentPlayerProfile[];
  steps: AgentStep[];
  metrics: AgentMetricComparison[];
  evidence: AgentEvidence[];
  recommendation: AgentRecommendation;
  generation: AgentGeneration;
  limitations: string[];
  sample_notice: string;
}

export interface AgentAnalysisRequest {
  question: string;
  player_slugs: [string, string];
  season: string;
  focus: AgentRequestedFocus;
}
