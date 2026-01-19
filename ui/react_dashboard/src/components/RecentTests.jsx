import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { CheckCircle, XCircle, SkipForward, ExternalLink, Eye } from 'lucide-react'

const statusEmojis = {
  PASSED: '✅',
  FAILED: '❌',
  SKIPPED: '⏭️',
  RUNNING: '⚡',
}

const statusColors = {
  PASSED: 'border-green-500 bg-green-500/10',
  FAILED: 'border-red-500 bg-red-500/10',
  SKIPPED: 'border-yellow-500 bg-yellow-500/10',
  RUNNING: 'border-blue-500 bg-blue-500/10',
}

export default function RecentTests({ tests = [] }) {
  const navigate = useNavigate()

  const handleViewDetails = (test) => {
    navigate(`/results?test=${encodeURIComponent(test.name)}&status=${test.status}`)
  }

  if (tests.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="glass rounded-2xl p-6"
      >
        <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
          <span>🧪</span> Recent Test Results
        </h2>
        <div className="text-center py-12 text-gray-400">
          <motion.div
            animate={{ rotate: [0, 360] }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="text-6xl mb-4"
          >
            🔄
          </motion.div>
          <p>No test results yet. Run some tests! 🎯</p>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="glass rounded-2xl p-6"
    >
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <span>🧪</span> Recent Test Results
      </h2>
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {tests.map((test, index) => (
          <motion.div
            key={test.id || index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.02, x: 5 }}
            className={`
              glass rounded-lg p-4 border-l-4
              ${statusColors[test.status] || statusColors.PASSED}
              card-hover cursor-pointer
            `}
            onClick={() => handleViewDetails(test)}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-2xl">
                    {statusEmojis[test.status] || '✅'}
                  </span>
                  <span className="font-semibold">{test.name}</span>
                  <span className="text-xs px-2 py-1 rounded-full bg-white/10">
                    {test.status}
                  </span>
                </div>
                <p className="text-sm text-gray-300 mb-2">
                  {test.suite || 'Unknown Suite'}
                </p>
                <div className="flex items-center gap-4 text-xs text-gray-400">
                  <span>⏱️ {test.duration || 'N/A'}</span>
                  <span>📅 {new Date(test.timestamp || Date.now()).toLocaleDateString()}</span>
                </div>
              </div>
              <motion.button
                whileHover={{ scale: 1.2, rotate: 15 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors"
                onClick={(e) => {
                  e.stopPropagation()
                  handleViewDetails(test)
                }}
                title="View Details"
              >
                <Eye className="w-4 h-4 text-gray-300" />
              </motion.button>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  )
}
