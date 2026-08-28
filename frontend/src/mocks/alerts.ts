import type { Alert } from "../types/alert";

export const mockAlerts: Alert[] = [
  {
    id: "ALERT-001",
    prediction_id: "PRED-001",
    location_id: "ATM-104",
    location_name: "ATM-104 / Location X",
    risk_score: 91,
    risk_level: "CRITICAL",
    predicted_window: "18:00-21:00",
    crime_category: "Financial Cyber Fraud",
    status: "NEW",
    title: "Critical withdrawal risk detected",
    description:
      "A critical-risk prediction has been generated for ATM-104 based on recent suspicious withdrawals, historical transaction patterns and geographic correlation.",
    created_at: "2026-08-28T14:05:00Z",
  },

  {
    id: "ALERT-002",
    prediction_id: "PRED-002",
    location_id: "ATM-221",
    location_name: "ATM-221 / Central Zone",
    risk_score: 86,
    risk_level: "CRITICAL",
    predicted_window: "20:00-23:00",
    crime_category: "ATM Fraud",
    status: "ACKNOWLEDGED",
    title: "High-priority ATM fraud prediction",
    description:
      "A critical prediction has been generated for ATM-221 following repeated suspicious transactions and elevated transaction velocity.",
    created_at: "2026-08-28T13:50:00Z",
    acknowledged_at: "2026-08-28T14:10:00Z",
    acknowledged_by: "LEA Officer",
  },

  {
    id: "ALERT-003",
    prediction_id: "PRED-003",
    location_id: "ATM-087",
    location_name: "ATM-087 / Market Area",
    risk_score: 68,
    risk_level: "HIGH",
    predicted_window: "16:00-19:00",
    crime_category: "UPI Fraud",
    status: "NEW",
    title: "Elevated UPI fraud risk",
    description:
      "Elevated risk has been detected around ATM-087 due to increased transaction activity, nearby complaints and unusual time-based behavior.",
    created_at: "2026-08-28T13:35:00Z",
  },

  {
    id: "ALERT-004",
    prediction_id: "PRED-007",
    location_id: "ATM-418",
    location_name: "ATM-418 / Commercial District",
    risk_score: 77,
    risk_level: "HIGH",
    predicted_window: "19:00-22:00",
    crime_category: "Financial Cyber Fraud",
    status: "NEW",
    title: "Suspicious withdrawal sequence detected",
    description:
      "Multiple high-value withdrawals and nearby fraud complaints have contributed to an elevated risk prediction for ATM-418.",
    created_at: "2026-08-28T12:20:00Z",
  },

  {
    id: "ALERT-005",
    prediction_id: "PRED-004",
    location_id: "ATM-312",
    location_name: "ATM-312 / University Zone",
    risk_score: 57,
    risk_level: "MEDIUM",
    predicted_window: "12:00-15:00",
    crime_category: "Card Fraud",
    status: "NEW",
    title: "Moderate card fraud risk",
    description:
      "A moderate-risk prediction has been generated based on transaction activity and a minor historical anomaly.",
    created_at: "2026-08-28T12:55:00Z",
  },

  {
    id: "ALERT-006",
    prediction_id: "PRED-005",
    location_id: "ATM-156",
    location_name: "ATM-156 / Station Road",
    risk_score: 43,
    risk_level: "MEDIUM",
    predicted_window: "10:00-13:00",
    crime_category: "Identity Theft",
    status: "ACKNOWLEDGED",
    title: "Identity theft risk identified",
    description:
      "A moderate risk signal has been identified from a minor behavioral anomaly and recent complaint activity.",
    created_at: "2026-08-28T12:35:00Z",
    acknowledged_at: "2026-08-28T13:05:00Z",
    acknowledged_by: "I4C Analyst",
  },
];

export const getAlertById = (
  id: string,
): Alert | undefined => {
  return mockAlerts.find(
    (alert) => alert.id === id,
  );
};

export const getAlertsByPredictionId = (
  predictionId: string,
): Alert[] => {
  return mockAlerts.filter(
    (alert) => alert.prediction_id === predictionId,
  );
};

export const getActiveAlerts = (): Alert[] => {
  return mockAlerts.filter(
    (alert) => alert.status === "NEW",
  );
};

export const getAcknowledgedAlerts = (): Alert[] => {
  return mockAlerts.filter(
    (alert) => alert.status === "ACKNOWLEDGED",
  );
};