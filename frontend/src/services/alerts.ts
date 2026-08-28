import type {
  Alert,
} from "../types/alert";

import {
  mockAlerts,
} from "../mocks/alerts";

import {
  apiRequest,
} from "./api";

const USE_MOCK_DATA = true;

let alertsState: Alert[] = [
  ...mockAlerts,
];

export interface AlertFilters {
  risk_level?: string;
  status?: string;
}

export const getAlerts =
  async (
    filters?: AlertFilters,
  ): Promise<Alert[]> => {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) =>
        setTimeout(resolve, 300),
      );

      let results = [
        ...alertsState,
      ];

      if (filters?.risk_level) {
        results = results.filter(
          (alert) =>
            alert.risk_level ===
            filters.risk_level,
        );
      }

      if (filters?.status) {
        results = results.filter(
          (alert) =>
            alert.status ===
            filters.status,
        );
      }

      return results;
    }

    const params =
      new URLSearchParams();

    if (filters?.risk_level) {
      params.set(
        "risk_level",
        filters.risk_level,
      );
    }

    if (filters?.status) {
      params.set(
        "status",
        filters.status,
      );
    }

    const query =
      params.toString();

    return apiRequest<Alert[]>(
      `/alerts${query ? `?${query}` : ""}`,
    );
  };

export const getAlertById =
  async (
    id: string,
  ): Promise<Alert> => {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) =>
        setTimeout(resolve, 250),
      );

      const alert =
        alertsState.find(
          (item) => item.id === id,
        );

      if (!alert) {
        throw new Error(
          "Alert not found.",
        );
      }

      return alert;
    }

    return apiRequest<Alert>(
      `/alerts/${id}`,
    );
  };

export const acknowledgeAlert =
  async (
    id: string,
    acknowledgedBy: string,
  ): Promise<Alert> => {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) =>
        setTimeout(resolve, 500),
      );

      const index =
        alertsState.findIndex(
          (alert) =>
            alert.id === id,
        );

      if (index === -1) {
        throw new Error(
          "Alert not found.",
        );
      }

      const updatedAlert: Alert = {
        ...alertsState[index],
        status: "ACKNOWLEDGED",
        acknowledged_at:
          new Date().toISOString(),
        acknowledged_by:
          acknowledgedBy,
      };

      alertsState[index] =
        updatedAlert;

      return updatedAlert;
    }

    return apiRequest<Alert>(
      `/alerts/${id}/acknowledge`,
      {
        method: "POST",
        body: JSON.stringify({
          acknowledged_by:
            acknowledgedBy,
        }),
      },
    );
  };