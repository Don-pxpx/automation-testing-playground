export type TestStatus = 'PASSED' | 'FAILED' | 'SKIPPED' | 'XFAILED' | 'UNKNOWN';

export interface TestCaseMetric {
  nodeid: string;
  name: string;
  suite: string;
  requirementId: string | null;
  status: TestStatus;
  durationSeconds: number;
  timestamp: string;
}

export interface SuiteSummary {
  passed: number;
  failed: number;
  skipped: number;
  xfailed: number;
  total: number;
}

export interface RunSummary {
  total: number;
  passed: number;
  failed: number;
  skipped: number;
  xfailed: number;
  passRate: number;
}

export interface TestRunMetrics {
  runId: string;
  timestamp: string;
  exitStatus: number;
  durationSeconds: number;
  summary: RunSummary;
  bySuite: Record<string, SuiteSummary>;
  byRequirement: Record<string, TestStatus>;
  tests: TestCaseMetric[];
}

export interface DashboardMetricsView {
  headline: RunSummary & { durationSeconds: number; requirementCount: number };
  suiteChart: Array<{
    suite: string;
    passed: number;
    failed: number;
    skipped: number;
    xfailed: number;
  }>;
  requirementCoverage: Array<{
    requirementId: string;
    status: TestStatus;
  }>;
}
