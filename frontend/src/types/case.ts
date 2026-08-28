import type { RiskLevel } from "./prediction";

export type CaseStatus = "ACTIVE" | "UNDER_REVIEW" | "CLOSED";

export interface Complaint {
  id: string;

  title: string;

  category: string;

  location?: string;

  created_at: string;

  status: string;
}

export interface TimelineEvent {
  id: string;

  timestamp: string;

  event: string;

  location: string;

  type?: string;
}

export interface IntelligenceNote {
  id: string;

  author: string;

  note: string;

  created_at: string;
}

export interface InvestigationCase {
  id: string;

  case_number: string;

  status: CaseStatus;

  risk_level: RiskLevel;

  risk_score: number;

  related_complaints: Complaint[];

  predicted_hotspots: string[];

  timeline: TimelineEvent[];

  intelligence_notes: IntelligenceNote[];

  created_at: string;

  updated_at: string;
}