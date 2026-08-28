import type {
  DashboardData,
} from "../types/dashboard";

import {
  mockDashboardData,
} from "../mocks/dashboard";

import {
  apiRequest,
} from "./api";

const USE_MOCK_DATA = true;

export const getDashboardData =
  async (): Promise<DashboardData> => {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) =>
        setTimeout(resolve, 350),
      );

      return mockDashboardData;
    }

    return apiRequest<DashboardData>(
      "/dashboard/summary",
    );
  };