import type { InvestigationCase } from "../types/case";

export const mockCases: InvestigationCase[] = [
  {
    id: "CASE-001",

    case_number: "CYB-2026-1024",

    status: "ACTIVE",

    risk_level: "CRITICAL",

    risk_score: 91,

    related_complaints: [
      {
        id: "C102",
        title: "Suspicious ATM withdrawal",
        category: "Financial Cyber Fraud",
        location: "Vijayawada",
        created_at: "2026-08-26T09:30:00Z",
        status: "OPEN",
      },

      {
        id: "C183",
        title: "Unauthorized account withdrawal",
        category: "Financial Cyber Fraud",
        location: "Vijayawada",
        created_at: "2026-08-26T13:15:00Z",
        status: "UNDER REVIEW",
      },

      {
        id: "C201",
        title: "Multiple suspicious transactions",
        category: "Financial Cyber Fraud",
        location: "Vijayawada",
        created_at: "2026-08-27T10:45:00Z",
        status: "OPEN",
      },
    ],

    predicted_hotspots: [
      "ATM-104",
      "ATM-221",
    ],

    timeline: [
      {
        id: "EVENT-001",
        timestamp: "2026-08-26T09:30:00Z",
        event: "Complaint C102 registered",
        location: "Vijayawada",
        type: "COMPLAINT",
      },

      {
        id: "EVENT-002",
        timestamp: "2026-08-26T11:45:00Z",
        event: "Suspicious withdrawal pattern detected",
        location: "ATM-104",
        type: "DETECTION",
      },

      {
        id: "EVENT-003",
        timestamp: "2026-08-26T13:15:00Z",
        event: "Complaint C183 registered",
        location: "Vijayawada",
        type: "COMPLAINT",
      },

      {
        id: "EVENT-004",
        timestamp: "2026-08-27T10:45:00Z",
        event: "Complaint C201 registered",
        location: "Vijayawada",
        type: "COMPLAINT",
      },

      {
        id: "EVENT-005",
        timestamp: "2026-08-28T14:00:00Z",
        event: "Critical prediction generated for ATM-104",
        location: "ATM-104",
        type: "PREDICTION",
      },

      {
        id: "EVENT-006",
        timestamp: "2026-08-28T14:05:00Z",
        event: "Critical alert generated",
        location: "ATM-104",
        type: "ALERT",
      },
    ],

    intelligence_notes: [
      {
        id: "NOTE-001",
        author: "LEA Officer",
        note:
          "Recent withdrawal activity around ATM-104 shows a strong similarity to previously observed fraud patterns.",
        created_at: "2026-08-28T14:10:00Z",
      },

      {
        id: "NOTE-002",
        author: "I4C Analyst",
        note:
          "Geographic correlation with related complaints increases the confidence of the current prediction.",
        created_at: "2026-08-28T14:15:00Z",
      },

      {
        id: "NOTE-003",
        author: "LEA Officer",
        note:
          "Recommended action: review ATM-104 activity during the predicted 18:00-21:00 window.",
        created_at: "2026-08-28T14:20:00Z",
      },
    ],

    created_at: "2026-08-26T09:30:00Z",

    updated_at: "2026-08-28T14:20:00Z",
  },
];

export const getCaseById = (
  id: string,
): InvestigationCase | undefined => {
  return mockCases.find(
    (investigationCase) =>
      investigationCase.id === id,
  );
};

export const getCaseByCaseNumber = (
  caseNumber: string,
): InvestigationCase | undefined => {
  return mockCases.find(
    (investigationCase) =>
      investigationCase.case_number === caseNumber,
  );
};