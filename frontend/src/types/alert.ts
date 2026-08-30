import type { RiskLevel } from "./prediction";

export type AlertStatus = "NEW" | "ACKNOWLEDGED";

export interface Alert {
  id: string;

  prediction_id: string;

  location_id: string;

  location_name: string;

  risk_score: number;

  risk_level: RiskLevel;

  predicted_window: string;

  crime_category: string;

  status: AlertStatus;

  title: string;

  description: string;

  created_at: string;

  acknowledged_at?: string;

  acknowledged_by?: string;
}