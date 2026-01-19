import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Clock, CheckCircle, XCircle, Zap } from 'lucide-react'
import { getTestHistory } from '../utils/api'

export default function TestHistory() {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const data = await getTestHistory()
      setHistory(data)
      setLoading(false)
    } catch (error) {
      console.error('Failed to load history:', error)
      setLoading(false)
    }
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
                <div className="flex items-center gap-4">
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="text-4xl"
                  >
                    {statusEmojis[run.status] || '⚡'}
                  </motion.div>
                  <div>
                    <h3 className="text-xl font-bold mb-1">{run.suite || 'Test Run'}</h3>
                    <p className="text-gray-400 text-sm">
                      🧪 {run.totalTests || 0} tests • ⏱️ {run.duration || 'N/A'}
                    </p>
                    <p className="text-gray-500 text-xs mt-1">
                      ✅ {run.passed || 0} passed • ❌ {run.failed || 0} failed • ⏭️ {run.skipped || 0} skipped
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <span className={`font-semibold ${statusColors[run.status]}`}>
                    {run.status}
                  </span>
                  <p className="text-xs text-gray-400 mt-1">
                    {new Date(run.timestamp || Date.now()).toLocaleString()}
                  </p>
                </div>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </motion.div>
  )
}
