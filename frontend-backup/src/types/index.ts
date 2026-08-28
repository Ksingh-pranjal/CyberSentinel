export type RiskLevel='LOW'|'MEDIUM'|'HIGH'|'CRITICAL'; export type Role='LEA Officer'|'Bank/FI'|'I4C Analyst'; export type AlertStatus='NEW'|'ACKNOWLEDGED';
export interface User { id:string; name:string; email:string; role:Role; }
export interface Prediction { id:string; location_id:string; location_name:string; region:string; latitude:number; longitude:number; risk_score:number; risk_level:RiskLevel; predicted_window:string; crime_category:string; rank:number; top_factors:string[]; related_complaints:string[]; model_version:string; confidence:number; case_id:string; }
export interface Alert { id:string; prediction_id:string; severity:RiskLevel; status:AlertStatus; created_at:string; }
export interface Case { id:string; status:'ACTIVE'|'PENDING'|'CLOSED'; summary:string; risk_level:RiskLevel; complaints:string[]; hotspot_ids:string[]; notes:string[]; timeline:{time:string; event:string; location:string}[]; }
export interface DashboardSummary { totalComplaints:number; highRiskZones:number; activeAlerts:number; atRiskAtms:number; }
export interface Filters {region:string; category:string; window:string; risk:string}
