/**
 * Formats an ISO date/time string for the dashboard.
 *
 * Example:
 * 2026-08-28T14:05:00Z
 * -> "28 Aug 2026, 7:35 PM"
 */
export const formatDateTime = (
  value: string,
): string => {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "—";
  }

  return new Intl.DateTimeFormat(
    "en-IN",
    {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    },
  ).format(date);
};

/**
 * Formats a date without the time.
 */
export const formatDate = (
  value: string,
): string => {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "—";
  }

  return new Intl.DateTimeFormat(
    "en-IN",
    {
      day: "2-digit",
      month: "short",
      year: "numeric",
    },
  ).format(date);
};

/**
 * Converts a time range into a cleaner display format.
 *
 * Example:
 * "18:00-21:00"
 * -> "18:00 – 21:00"
 */
export const formatTimeWindow = (
  value: string,
): string => {
  if (!value) {
    return "—";
  }

  return value.replace(
    /(\d{2}:\d{2})-(\d{2}:\d{2})/,
    "$1 – $2",
  );
};

/**
 * Formats large numbers for KPI cards.
 *
 * Example:
 * 8240 -> "8,240"
 */
export const formatNumber = (
  value: number,
): string => {
  return new Intl.NumberFormat(
    "en-IN",
  ).format(value);
};

/**
 * Formats a decimal confidence value.
 *
 * Example:
 * 0.94 -> "94%"
 *
 * Also accepts an already-normalized percentage:
 * 94 -> "94%"
 */
export const formatConfidence = (
  value: number,
): string => {
  const percentage =
    value >= 0 && value <= 1
      ? value * 100
      : value;

  return `${Math.round(percentage)}%`;
};

/**
 * Converts a technical role identifier into
 * a user-friendly label.
 */
export const formatRole = (
  role: string,
): string => {
  switch (role) {
    case "LEA_OFFICER":
      return "LEA Officer";

    case "BANK_FI":
      return "Bank / FI";

    case "I4C_ANALYST":
      return "I4C Analyst";

    default:
      return role;
  }
};