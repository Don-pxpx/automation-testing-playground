import { buildDashboardView, type DashboardMetricsView, type TestRunMetrics } from '@reporting/index';

export type { DashboardMetricsView, TestRunMetrics };

export function toDashboardView(metrics: TestRunMetrics): DashboardMetricsView {
  return buildDashboardView(metrics);
}

export function emptyMetrics(): TestRunMetrics {
  return {
    runId: '',
    timestamp: new Date().toISOString(),
    exitStatus: 0,
    durationSeconds: 0,
    summary: {
      total: 0,
      passed: 0,
      failed: 0,
      skipped: 0,
      xfailed: 0,
      passRate: 0,
    },
    bySuite: {},
    byRequirement: {},
    tests: [],
  };
}
