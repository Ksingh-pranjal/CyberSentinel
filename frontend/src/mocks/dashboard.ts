import type {
  DashboardData,
  DashboardSummary,
  RiskTrendPoint,
  TopPredictedLocation,
} from "../types/dashboard";

export const mockDashboardSummary: DashboardSummary = {
  total_complaints: 8240,
  high_risk_zones: 27,
  active_alerts: 14,
  at_risk_atms: 42,
};

export const mockRiskTrend: RiskTrendPoint[] = [
  {
    date: "Aug 22",
    risk_score: 48,
    high_risk_predictions: 8,
  },
  {
    date: "Aug 23",
    risk_score: 52,
    high_risk_predictions: 10,
  },
  {
    date: "Aug 24",
    risk_score: 56,
    high_risk_predictions: 12,
  },
  {
    date: "Aug 25",
    risk_score: 61,
    high_risk_predictions: 15,
  },
  {
    date: "Aug 26",
    risk_score: 58,
    high_risk_predictions: 13,
  },
  {
    date: "Aug 27",
    risk_score: 67,
    high_risk_predictions: 19,
  },
  {
    date: "Aug 28",
    risk_score: 72,
    high_risk_predictions: 23,
  },
];

export const mockTopPredictedLocations: TopPredictedLocation[] = [
  {
    prediction_id: "PRED-001",
    location_id: "ATM-104",
    location_name: "ATM-104",
    risk_score: 91,
    risk_level: "CRITICAL",
    predicted_window: "18:00-21:00",
  },
  {
    prediction_id: "PRED-002",
    location_id: "ATM-221",
    location_name: "ATM-221",
    risk_score: 86,
    risk_level: "CRITICAL",
    predicted_window: "20:00-23:00",
  },
  {
    prediction_id: "PRED-007",
    location_id: "ATM-418",
    location_name: "ATM-418",
    risk_score: 77,
    risk_level: "HIGH",
    predicted_window: "19:00-22:00",
  },
  {
    prediction_id: "PRED-003",
    location_id: "ATM-087",
    location_name: "ATM-087",
    risk_score: 68,
    risk_level: "HIGH",
    predicted_window: "16:00-19:00",
  },
  {
    prediction_id: "PRED-004",
    location_id: "ATM-312",
    location_name: "ATM-312",
    risk_score: 57,
    risk_level: "MEDIUM",
    predicted_window: "12:00-15:00",
  },
];

export const mockDashboardData: DashboardData = {
  summary: mockDashboardSummary,
  risk_trend: mockRiskTrend,
  top_predicted_locations: mockTopPredictedLocations,
};