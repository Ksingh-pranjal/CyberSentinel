export type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export type CrimeCategory =
  | "Financial Cyber Fraud"
  | "UPI Fraud"
  | "ATM Fraud"
  | "Card Fraud"
  | "Identity Theft"
  | "Other";

export interface PredictionFactor {
  name: string;
  description?: string;
  impact?: "LOW" | "MEDIUM" | "HIGH";
}

export interface Prediction {
  id: string;

  location_id: string;

  location_name: string;

  latitude: number;

  longitude: number;

  region: string;

  crime_category: CrimeCategory;

  risk_score: number;

  risk_level: RiskLevel;

  predicted_window: string;

  rank: number;

  confidence: number;

  top_factors: string[];

  factors?: PredictionFactor[];

  related_complaints: string[];

  model_version: string;

  created_at: string;

  updated_at: string;
}