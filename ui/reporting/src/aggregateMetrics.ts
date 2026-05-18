import type { DashboardMetricsView, TestRunMetrics } from './types.js';

export function buildDashboardView(metrics: TestRunMetrics): DashboardMetricsView {
  const suiteChart = Object.entries(metrics.bySuite).map(([suite, counts]) => ({
    suite,
    passed: counts.passed,
    failed: counts.failed,
    skipped: counts.skipped,
    xfailed: counts.xfailed,
  }));

  const requirementCoverage = Object.entries(metrics.byRequirement).map(
    ([requirementId, status]) => ({ requirementId, status }),
  );

  return {
    headline: {
      ...metrics.summary,
      durationSeconds: metrics.durationSeconds,
      requirementCount: requirementCoverage.length,
    },
    suiteChart,
    requirementCoverage,
  };
}

export function formatPassRate(passRate: number): string {
  return `${passRate.toFixed(1)}%`;
}
