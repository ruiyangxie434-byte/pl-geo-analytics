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
