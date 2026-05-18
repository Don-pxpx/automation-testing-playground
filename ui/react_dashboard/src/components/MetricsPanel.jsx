import { motion } from 'framer-motion'

export default function MetricsPanel({ view }) {
  if (!view) return null

  const { headline, suiteChart, requirementCoverage } = view

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-2xl p-6 space-y-4"
    >
      <h3 className="text-xl font-bold flex items-center gap-2">
        <span>📈</span> Reporting metrics
      </h3>

      <motion.div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
        <div className="rounded-xl bg-white/5 p-3">
          <p className="text-gray-400 text-sm">Duration</p>
          <p className="text-2xl font-bold">{headline.durationSeconds}s</p>
        </motion.div>
        <div className="rounded-xl bg-white/5 p-3">
          <p className="text-gray-400 text-sm">Requirements</p>
          <p className="text-2xl font-bold">{headline.requirementCount}</p>
        </motion.div>
        <motion.div className="rounded-xl bg-amber-500/10 p-3">
          <p className="text-amber-300 text-sm">Expected issues</p>
          <p className="text-2xl font-bold text-amber-200">{headline.xfailed}</p>
        </motion.div>
        <div className="rounded-xl bg-emerald-500/10 p-3">
          <p className="text-emerald-300 text-sm">Pass rate</p>
          <p className="text-2xl font-bold text-emerald-200">{headline.passRate.toFixed(1)}%</p>
        </motion.div>
      </motion.div>

      {suiteChart.length > 0 && (
        <motion.div>
          <p className="text-gray-400 text-sm mb-2">By application</p>
          <div className="flex flex-wrap gap-2">
            {suiteChart.map((row) => (
              <span
                key={row.suite}
                className="px-3 py-1 rounded-full bg-purple-500/20 text-sm border border-purple-500/30"
              >
                {row.suite}: ✅ {row.passed} ❌ {row.failed} ⚠️ {row.xfailed}
              </span>
            ))}
          </div>
        </motion.div>
      )}

      {requirementCoverage.length > 0 && (
        <motion.div>
          <p className="text-gray-400 text-sm mb-2">Requirement IDs (latest run)</p>
          <div className="max-h-32 overflow-y-auto flex flex-wrap gap-1">
            {requirementCoverage.slice(0, 12).map((item) => (
              <span
                key={item.requirementId}
                className="text-xs px-2 py-0.5 rounded bg-slate-700/80"
                title={item.status}
              >
                {item.requirementId}
              </span>
            ))}
            {requirementCoverage.length > 12 && (
              <span className="text-xs text-gray-500">+{requirementCoverage.length - 12} more</span>
            )}
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}
