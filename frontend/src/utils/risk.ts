import type {
  RiskLevel,
} from "../types/prediction";

/**
 * Converts a numerical risk score into a risk level.
 *
 * Risk scale:
 * 0-39   LOW
 * 40-59  MEDIUM
 * 60-79  HIGH
 * 80-100 CRITICAL
 */
export const getRiskLevel = (
  score: number,
): RiskLevel => {
  const normalizedScore = Math.max(
    0,
    Math.min(100, score),
  );

  if (normalizedScore >= 80) {
    return "CRITICAL";
  }

  if (normalizedScore >= 60) {
    return "HIGH";
  }

  if (normalizedScore >= 40) {
    return "MEDIUM";
  }

  return "LOW";
};

/**
 * Returns a human-readable risk label.
 */
export const getRiskLabel = (
  level: RiskLevel,
): string => {
  switch (level) {
    case "CRITICAL":
      return "Critical";

    case "HIGH":
      return "High";

    case "MEDIUM":
      return "Medium";

    case "LOW":
      return "Low";

    default:
      return "Unknown";
  }
};

/**
 * Returns Tailwind utility classes for a risk badge.
 *
 * We keep the strong warning colors restricted to actual
 * risk states as requested by the UI specification.
 */
export const getRiskStyles = (
  level: RiskLevel,
) => {
  switch (level) {
    case "CRITICAL":
      return {
        badge:
          "border-red-500/30 bg-red-500/15 text-red-400",
        dot: "bg-red-500",
        text: "text-red-400",
        border: "border-red-500/40",
        background: "bg-red-500/10",
      };

    case "HIGH":
      return {
        badge:
          "border-orange-500/30 bg-orange-500/15 text-orange-400",
        dot: "bg-orange-500",
        text: "text-orange-400",
        border: "border-orange-500/40",
        background: "bg-orange-500/10",
      };

    case "MEDIUM":
      return {
        badge:
          "border-yellow-500/30 bg-yellow-500/15 text-yellow-400",
        dot: "bg-yellow-500",
        text: "text-yellow-400",
        border: "border-yellow-500/40",
        background: "bg-yellow-500/10",
      };

    case "LOW":
      return {
        badge:
          "border-emerald-500/30 bg-emerald-500/15 text-emerald-400",
        dot: "bg-emerald-500",
        text: "text-emerald-400",
        border: "border-emerald-500/40",
        background: "bg-emerald-500/10",
      };

    default:
      return {
        badge:
          "border-gray-500/30 bg-gray-500/15 text-gray-400",
        dot: "bg-gray-500",
        text: "text-gray-400",
        border: "border-gray-500/40",
        background: "bg-gray-500/10",
      };
  }
};

/**
 * Returns the numerical risk score as a percentage.
 *
 * Accepts both:
 *   91
 *   0.91
 *
 * This makes the frontend tolerant of either the current
 * mock-data representation or a normalized backend response.
 */
export const normalizeRiskScore = (
  score: number,
): number => {
  if (score >= 0 && score <= 1) {
    return Math.round(score * 100);
  }

  return Math.round(
    Math.max(0, Math.min(100, score)),
  );
};

/**
 * Returns a risk score formatted for the UI.
 *
 * Example:
 * 91 -> "91/100"
 */
export const formatRiskScore = (
  score: number,
): string => {
  return `${normalizeRiskScore(score)}/100`;
};

/**
 * Returns a risk level based on a score.
 *
 * Useful when the backend doesn't explicitly provide
 * risk_level.
 */
export const getRiskLevelFromScore = (
  score: number,
): RiskLevel => {
  return getRiskLevel(
    normalizeRiskScore(score),
  );
};