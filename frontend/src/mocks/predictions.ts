import type { Prediction } from "../types/prediction";

export const mockPredictions: Prediction[] = [
  {
    id: "PRED-001",
    location_id: "ATM-104",
    location_name: "ATM-104 / Location X",
    latitude: 16.5062,
    longitude: 80.648,
    region: "Vijayawada",
    crime_category: "Financial Cyber Fraud",
    risk_score: 91,
    risk_level: "CRITICAL",
    predicted_window: "18:00-21:00",
    rank: 1,
    confidence: 94,
    top_factors: [
      "Recent suspicious withdrawals nearby",
      "Similar historical transaction pattern",
      "High recent transaction activity",
      "Strong geographic correlation",
    ],
    factors: [
      {
        name: "Recent suspicious withdrawals",
        description:
          "Multiple suspicious withdrawal events were detected in the surrounding area.",
        impact: "HIGH",
      },
      {
        name: "Historical transaction pattern",
        description:
          "The current transaction pattern is similar to previously observed fraudulent activity.",
        impact: "HIGH",
      },
      {
        name: "Recent transaction activity",
        description:
          "Transaction activity has increased significantly during the recent observation window.",
        impact: "HIGH",
      },
      {
        name: "Geographic correlation",
        description:
          "The location has a strong geographic correlation with nearby reported incidents.",
        impact: "MEDIUM",
      },
    ],
    related_complaints: ["C102", "C183", "C201"],
    model_version: "xgb_v1",
    created_at: "2026-08-28T14:00:00Z",
    updated_at: "2026-08-28T14:05:00Z",
  },

  {
    id: "PRED-002",
    location_id: "ATM-221",
    location_name: "ATM-221 / Central Zone",
    latitude: 17.385,
    longitude: 78.4867,
    region: "Hyderabad",
    crime_category: "ATM Fraud",
    risk_score: 86,
    risk_level: "CRITICAL",
    predicted_window: "20:00-23:00",
    rank: 2,
    confidence: 91,
    top_factors: [
      "Repeated suspicious transactions",
      "High transaction velocity",
      "Historical fraud similarity",
    ],
    factors: [
      {
        name: "Repeated suspicious transactions",
        description:
          "Several transactions matching suspicious behavioral patterns were observed.",
        impact: "HIGH",
      },
      {
        name: "Transaction velocity",
        description:
          "The number of recent transactions is above the expected baseline.",
        impact: "HIGH",
      },
      {
        name: "Historical fraud similarity",
        description:
          "Recent activity resembles previously observed ATM fraud patterns.",
        impact: "MEDIUM",
      },
    ],
    related_complaints: ["C221", "C245"],
    model_version: "xgb_v1",
    created_at: "2026-08-28T13:45:00Z",
    updated_at: "2026-08-28T13:55:00Z",
  },

  {
    id: "PRED-003",
    location_id: "ATM-087",
    location_name: "ATM-087 / Market Area",
    latitude: 17.6868,
    longitude: 83.2185,
    region: "Visakhapatnam",
    crime_category: "UPI Fraud",
    risk_score: 68,
    risk_level: "HIGH",
    predicted_window: "16:00-19:00",
    rank: 3,
    confidence: 82,
    top_factors: [
      "Increased transaction activity",
      "Nearby complaints",
      "Unusual time-based pattern",
    ],
    factors: [
      {
        name: "Increased transaction activity",
        description:
          "Transaction activity has increased compared with the recent baseline.",
        impact: "HIGH",
      },
      {
        name: "Nearby complaints",
        description:
          "Several cybercrime complaints have been recorded in the surrounding area.",
        impact: "MEDIUM",
      },
      {
        name: "Time-based pattern",
        description:
          "The current activity overlaps with a previously observed suspicious time window.",
        impact: "MEDIUM",
      },
    ],
    related_complaints: ["C087", "C114"],
    model_version: "xgb_v1",
    created_at: "2026-08-28T13:30:00Z",
    updated_at: "2026-08-28T13:40:00Z",
  },

  {
    id: "PRED-004",
    location_id: "ATM-312",
    location_name: "ATM-312 / University Zone",
    latitude: 16.5062,
    longitude: 80.621,
    region: "Vijayawada",
    crime_category: "Card Fraud",
    risk_score: 57,
    risk_level: "MEDIUM",
    predicted_window: "12:00-15:00",
    rank: 4,
    confidence: 76,
    top_factors: [
      "Moderate transaction activity",
      "Historical anomaly",
    ],
    factors: [
      {
        name: "Moderate transaction activity",
        description:
          "Transaction volume is moderately above the expected baseline.",
        impact: "MEDIUM",
      },
      {
        name: "Historical anomaly",
        description:
          "A minor deviation from historical behavior has been detected.",
        impact: "LOW",
      },
    ],
    related_complaints: ["C312"],
    model_version: "xgb_v1",
    created_at: "2026-08-28T12:50:00Z",
    updated_at: "2026-08-28T13:00:00Z",
  },

  {
    id: "PRED-005",
    location_id: "ATM-156",
    location_name: "ATM-156 / Station Road",
    latitude: 17.4126,
    longitude: 78.4071,
    region: "Hyderabad",
    crime_category: "Identity Theft",
    risk_score: 43,
    risk_level: "MEDIUM",
    predicted_window: "10:00-13:00",
    rank: 5,
    confidence: 69,
    top_factors: [
      "Minor behavioral anomaly",
      "Recent complaint activity",
    ],
    factors: [
      {
        name: "Behavioral anomaly",
        description:
          "A small deviation from the expected transaction behavior was detected.",
        impact: "LOW",
      },
      {
        name: "Recent complaint activity",
        description:
          "A small number of complaints were reported in the surrounding area.",
        impact: "LOW",
      },
    ],
    related_complaints: ["C156"],
    model_version: "xgb_v1",
    created_at: "2026-08-28T12:30:00Z",
    updated_at: "2026-08-28T12:45:00Z",
  },

  {
    id: "PRED-006",
    location_id: "ATM-203",
    location_name: "ATM-203 / Residential Zone",
    latitude: 16.5193,
    longitude: 80.6305,
    region: "Vijayawada",
    crime_category: "Other",
    risk_score: 32,
    risk_level: "LOW",
    predicted_window: "09:00-12:00",
    rank: 6,
    confidence: 61,
    top_factors: [
      "Normal transaction behavior",
      "Low recent complaint activity",
    ],
    factors: [
      {
        name: "Transaction behavior",
        description:
          "Observed transaction behavior remains within the expected range.",
        impact: "LOW",
      },
      {
        name: "Complaint activity",
        description:
          "Very few relevant complaints have been observed nearby.",
        impact: "LOW",
      },
    ],
    related_complaints: [],
    model_version: "xgb_v1",
    created_at: "2026-08-28T11:30:00Z",
    updated_at: "2026-08-28T11:45:00Z",
  },

  {
    id: "PRED-007",
    location_id: "ATM-418",
    location_name: "ATM-418 / Commercial District",
    latitude: 17.431,
    longitude: 78.401,
    region: "Hyderabad",
    crime_category: "Financial Cyber Fraud",
    risk_score: 77,
    risk_level: "HIGH",
    predicted_window: "19:00-22:00",
    rank: 7,
    confidence: 88,
    top_factors: [
      "High-value transaction activity",
      "Suspicious withdrawal sequence",
      "Nearby fraud complaints",
    ],
    factors: [
      {
        name: "High-value transaction activity",
        description:
          "Recent transactions include values significantly above the local baseline.",
        impact: "HIGH",
      },
      {
        name: "Suspicious withdrawal sequence",
        description:
          "Multiple withdrawals occurred within a short period.",
        impact: "HIGH",
      },
      {
        name: "Nearby fraud complaints",
        description:
          "Recent complaints indicate increased fraud activity around this area.",
        impact: "MEDIUM",
      },
    ],
    related_complaints: ["C418", "C422", "C431"],
    model_version: "xgb_v1",
    created_at: "2026-08-28T11:15:00Z",
    updated_at: "2026-08-28T11:30:00Z",
  },

  {
    id: "PRED-008",
    location_id: "ATM-509",
    location_name: "ATM-509 / Port Area",
    latitude: 17.7041,
    longitude: 83.2977,
    region: "Visakhapatnam",
    crime_category: "UPI Fraud",
    risk_score: 24,
    risk_level: "LOW",
    predicted_window: "14:00-17:00",
    rank: 8,
    confidence: 58,
    top_factors: [
      "Stable transaction pattern",
      "No significant anomaly detected",
    ],
    factors: [
      {
        name: "Stable transaction pattern",
        description:
          "Recent transaction behavior is consistent with the historical baseline.",
        impact: "LOW",
      },
      {
        name: "Anomaly detection",
        description:
          "No significant suspicious pattern has been detected.",
        impact: "LOW",
      },
    ],
    related_complaints: [],
    model_version: "xgb_v1",
    created_at: "2026-08-28T10:45:00Z",
    updated_at: "2026-08-28T11:00:00Z",
  },
];

export const getPredictionById = (
  id: string,
): Prediction | undefined => {
  return mockPredictions.find(
    (prediction) => prediction.id === id,
  );
};

export const getPredictionByLocationId = (
  locationId: string,
): Prediction | undefined => {
  return mockPredictions.find(
    (prediction) => prediction.location_id === locationId,
  );
};