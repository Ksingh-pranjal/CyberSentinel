import type {
  InvestigationCase,
} from "../types/case";

import {
  mockCases,
} from "../mocks/cases";

import {
  apiRequest,
} from "./api";

const USE_MOCK_DATA = true;

export const getCase =
  async (
    id: string,
  ): Promise<InvestigationCase> => {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) =>
        setTimeout(resolve, 300),
      );

      const investigationCase =
        mockCases.find(
          (item) => item.id === id,
        );

      if (!investigationCase) {
        throw new Error(
          "Investigation case not found.",
        );
      }

      return investigationCase;
    }

    return apiRequest<InvestigationCase>(
      `/cases/${id}`,
    );
  };

export const getCaseByPrediction =
  async (
    predictionId: string,
  ): Promise<InvestigationCase> => {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) =>
        setTimeout(resolve, 300),
      );

      const investigationCase =
        mockCases.find(
          (item) =>
            item.predicted_hotspots.some(
              (hotspot) => {
                const normalized =
                  hotspot.toLowerCase();

                return (
                  normalized ===
                  predictionId.toLowerCase()
                );
              },
            ),
        );

      if (!investigationCase) {
        throw new Error(
          "No investigation case is linked to this prediction.",
        );
      }

      return investigationCase;
    }

    return apiRequest<InvestigationCase>(
      `/cases/by-prediction/${predictionId}`,
    );
  };