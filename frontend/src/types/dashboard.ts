export interface DashboardSummary {
  total_complaints: number;

  high_risk_zones: number;

  active_alerts: number;

  at_risk_atms: number;
}

export interface RiskTrendPoint {
  date: string;

  risk_score: number;

  high_risk_predictions: number;
}

export interface TopPredictedLocation {
  prediction_id: string;

  location_id: string;

  location_name: string;

  risk_score: number;

  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

  predicted_window: string;
}

export interface DashboardData {
  summary: DashboardSummary;

  risk_trend: RiskTrendPoint[];

  top_predicted_locations: TopPredictedLocation[];
}