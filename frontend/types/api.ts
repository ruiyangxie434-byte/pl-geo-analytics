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
  source_kind: "sample";
}

export interface ClubListData {
  items: ClubSummary[];
  total: number;
  player_total: number;
  limit: number;
  offset: number;
  sample_notice: string;
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
  source_kind: "sample";
}

export interface StandingTableData {
  season: string;
  items: StandingItem[];
  total: number;
  is_partial: boolean;
  sample_notice: string;
}

export type AgentFocus =
  | "balanced"
  | "scoring"
  | "creativity"
  | "pressing";

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

export interface AgentAnalysisData {
  run_id: string;
  task_type: "player_comparison";
  question: string;
  season: string;
  focus: AgentFocus;
  focus_label: string;
  players: AgentPlayerProfile[];
  steps: AgentStep[];
  metrics: AgentMetricComparison[];
  evidence: AgentEvidence[];
  recommendation: AgentRecommendation;
  limitations: string[];
  sample_notice: string;
}

export interface AgentAnalysisRequest {
  question: string;
  player_slugs: [string, string];
  season: string;
  focus: AgentFocus;
}
