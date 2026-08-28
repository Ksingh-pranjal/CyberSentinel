import type {
  Prediction,
} from "../types/prediction";

import {
  mockPredictions,
  getPredictionById,
} from "../mocks/predictions";

import {
  apiRequest,
} from "./api";

const USE_MOCK_DATA = true;

export interface PredictionFilters {
  region?: string;
  crime_category?: string;
  time_window?: string;
  risk_level?: string;
}

export const getPredictions =
  async (
    filters?: PredictionFilters,
  ): Promise<Prediction[]> => {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) =>
        setTimeout(resolve, 300),
      );

      let results = [
        ...mockPredictions,
      ];

      if (filters?.region) {
        results = results.filter(
          (prediction) =>
            prediction.region ===
            filters.region,
        );
      }

      if (filters?.crime_category) {
        results = results.filter(
          (prediction) =>
            prediction.crime_category ===
            filters.crime_category,
        );
      }

      if (filters?.time_window) {
        results = results.filter(
          (prediction) =>
            prediction.predicted_window ===
            filters.time_window,
        );
      }

      if (filters?.risk_level) {
        results = results.filter(
          (prediction) =>
            prediction.risk_level ===
            filters.risk_level,
        );
      }

      return results;
    }

    const params =
      new URLSearchParams();

    if (filters?.region) {
      params.set(
        "region",
        filters.region,
      );
    }

    if (filters?.crime_category) {
      params.set(
        "crime_category",
        filters.crime_category,
      );
    }

    if (filters?.time_window) {
      params.set(
        "time_window",
        filters.time_window,
      );
    }

    if (filters?.risk_level) {
      params.set(
        "risk_level",
        filters.risk_level,
      );
    }

    const query =
      params.toString();

    return apiRequest<Prediction[]>(
      `/predictions${query ? `?${query}` : ""}`,
    );
  };

export const getPrediction =
  async (
    id: string,
  ): Promise<Prediction> => {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) =>
        setTimeout(resolve, 300),
      );

      const prediction =
        getPredictionById(id);

      if (!prediction) {
        throw new Error(
          "Prediction not found.",
        );
      }

      return prediction;
    }

    return apiRequest<Prediction>(
      `/predictions/${id}`,
    );
  };

export const runPrediction =
  async (): Promise<Prediction[]> => {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) =>
        setTimeout(resolve, 800),
      );

      return mockPredictions;
    }

    return apiRequest<Prediction[]>(
      "/predictions/run",
      {
        method: "POST",
      },
    );
  };