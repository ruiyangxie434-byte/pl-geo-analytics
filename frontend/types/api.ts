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
