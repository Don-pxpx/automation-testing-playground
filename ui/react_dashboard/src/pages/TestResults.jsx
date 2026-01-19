import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Search, Filter } from 'lucide-react'
import { getAllTestResults } from '../utils/api'

export default function TestResults() {
  const [results, setResults] = useState([])
  const [filteredResults, setFilteredResults] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('ALL')
  const [suiteFilter, setSuiteFilter] = useState('ALL')

  useEffect(() => {
    loadResults()
  }, [])

  useEffect(() => {
    filterResults()
  }, [searchTerm, statusFilter, suiteFilter, results])

  const loadResults = async () => {
    try {
      const data = await getAllTestResults()
      setResults(data)
    } catch (error) {
      console.error('Failed to load test results:', error)
    }
  }

  const filterResults = () => {
    let filtered = results

    if (searchTerm) {
      filtered = filtered.filter(r =>
        r.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        r.suite.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (statusFilter !== 'ALL') {
      filtered = filtered.filter(r => r.status.toUpperCase() === statusFilter)
    }

    if (suiteFilter !== 'ALL') {
      filtered = filtered.filter(r => r.suite.toUpperCase() === suiteFilter.toUpperCase())
    }

    setFilteredResults(filtered)
  }

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

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <h1 className="text-4xl font-bold flex items-center gap-3">
          <span className="animate-pulse">🧪</span> All Test Results
        </h1>
      </div>

      {/* Search and Filter */}
      <div className="glass rounded-2xl p-4 flex gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="🔎 Search tests..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
        >
          <option value="ALL">All Statuses</option>
          <option value="PASSED">✅ Passed</option>
          <option value="FAILED">❌ Failed</option>
          <option value="SKIPPED">⏭️ Skipped</option>
        </select>
        <select
          value={suiteFilter}
          onChange={(e) => setSuiteFilter(e.target.value)}
          className="px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
        >
          <option value="ALL">All Suites</option>
          <option value="SauceDemo">SauceDemo</option>
          <option value="BlazeDemo">BlazeDemo</option>
          <option value="OrangeHRM">OrangeHRM</option>
          <option value="API">API</option>
        </select>
      </div>

      {/* Results List */}
      <div className="grid grid-cols-1 gap-4">
        {filteredResults.length === 0 ? (
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
            <p className="text-gray-400 text-lg">No test results found 🎯</p>
          </motion.div>
        ) : (
          filteredResults.map((result, index) => (
            <motion.div
              key={result.id || index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              whileHover={{ scale: 1.02, x: 5 }}
              className={`glass rounded-xl p-6 border-l-4 ${statusColors[result.status] || statusColors.PASSED} card-hover`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <span className="text-3xl">
                      {statusEmojis[result.status.toUpperCase()] || '✅'}
                    </span>
                    <h3 className="text-xl font-bold">{result.name}</h3>
                    <span className="px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 text-sm font-semibold">
                      {result.status}
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-4 text-sm text-gray-400 mb-2">
                    <span>📦 {result.suite || 'Unknown Suite'}</span>
                    <span>⏱️ {result.duration || 'N/A'}</span>
                    <span>📅 {new Date(result.timestamp || Date.now()).toLocaleString()}</span>
                  </div>
                  {result.error && (
                    <div className="mt-3 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
                      <p className="text-red-300 text-sm">{result.error}</p>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </motion.div>
  )
}
