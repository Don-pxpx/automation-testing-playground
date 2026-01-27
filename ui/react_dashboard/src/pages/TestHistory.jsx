import { useState, useEffect, useCallback } from 'react'
import { motion } from 'framer-motion'
import { Eye, RefreshCw, Download } from 'lucide-react'
import toast from 'react-hot-toast'
import { getTestHistory } from '../utils/api'

export default function TestHistory() {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  const loadHistory = useCallback(async () => {
    try {
      const data = await getTestHistory()
      // Validate data is an array
      if (Array.isArray(data)) {
        setHistory(data)
      } else {
        console.warn('API returned non-array data:', data)
        setHistory([])
      }
      setLoading(false)
    } catch (error) {
      console.error('Failed to load history:', error)
      setHistory([]) // Set empty array on error
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadHistory()
  }, [loadHistory])

  const handleViewDetails = (run) => {
    toast(
      (t) => (
        <div className="text-left">
          <div className="font-bold mb-2">Run details</div>
          <div className="text-sm space-y-1">
            <div><strong>Suite:</strong> {run.suite || 'Test Run'}</div>
            <div><strong>Passed:</strong> {run.passed ?? 0}</div>
            <div><strong>Failed:</strong> {run.failed ?? 0}</div>
            <div><strong>Skipped:</strong> {run.skipped ?? 0}</div>
            <div><strong>Duration:</strong> {run.duration ?? 'N/A'}</div>
          </div>
        </div>
      ),
      { duration: 5000, icon: '👁️' }
    )
  }

  const handleRerunSuite = (run) => {
    const suiteName = run.suite || 'Test Run'
    toast.loading(`Rerunning suite: ${suiteName}…`, { id: 'rerun' })
    setTimeout(() => {
      toast.success(`Rerun started: ${suiteName}`, { id: 'rerun' })
      loadHistory()
    }, 1500)
  }

  const handleDownloadReport = (run) => {
    const name = run.suite || 'Test Run'
    toast.success(`Download started for: ${name}`, { icon: '📥' })
  }

  const statusEmojis = {
    SUCCESS: '✅',
    FAILED: '❌',
    RUNNING: '⚡',
    PENDING: '⏳',
  }

  const statusColors = {
    SUCCESS: 'text-green-400',
    FAILED: 'text-red-400',
    RUNNING: 'text-yellow-400',
    PENDING: 'text-blue-400',
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="text-6xl"
        >
          ⚡
        </motion.div>
      </div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <h1 className="text-4xl font-bold flex items-center gap-3">
        <span className="animate-pulse">📜</span> Test History
      </h1>

      <div className="space-y-4">
        {history.length === 0 ? (
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="glass rounded-2xl p-12 text-center"
          >
            <motion.div
              animate={{ rotate: [0, 360] }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              className="text-6xl mb-4"
            >
              🔄
            </motion.div>
            <p className="text-gray-400 text-lg">No test history yet 🎯</p>
          </motion.div>
        ) : (
          history.map((run, index) => (
            <motion.div
              key={run.id || index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.02, x: 5 }}
              className="glass rounded-xl p-6 card-hover"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4 flex-1">
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="text-4xl"
                  >
                    {statusEmojis[run.status] || '⚡'}
                  </motion.div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold mb-1">{run.suite || 'Test Run'}</h3>
                    <p className="text-gray-400 text-sm">
                      🧪 {run.totalTests || 0} tests • ⏱️ {run.duration || 'N/A'}
                    </p>
                    <p className="text-gray-500 text-xs mt-1">
                      ✅ {run.passed || 0} passed • ❌ {run.failed || 0} failed • ⏭️ {run.skipped || 0} skipped
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right mr-4">
                    <span className={`font-semibold ${statusColors[run.status]}`}>
                      {run.status}
                    </span>
                    <p className="text-xs text-gray-400 mt-1">
                      {new Date(run.timestamp || Date.now()).toLocaleString()}
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => handleViewDetails(run)}
                      className="p-2 rounded-lg bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/50 transition-colors"
                      title="View Details"
                    >
                      <Eye className="w-4 h-4 text-blue-300" />
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => handleRerunSuite(run)}
                      className="p-2 rounded-lg bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/50 transition-colors"
                      title="Rerun Suite"
                    >
                      <RefreshCw className="w-4 h-4 text-purple-300" />
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => handleDownloadReport(run)}
                      className="p-2 rounded-lg bg-green-500/20 hover:bg-green-500/30 border border-green-500/50 transition-colors"
                      title="Download Report"
                    >
                      <Download className="w-4 h-4 text-green-300" />
                    </motion.button>
                  </div>
                </div>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </motion.div>
  )
}
