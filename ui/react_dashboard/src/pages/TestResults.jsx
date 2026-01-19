import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Search, Filter, Eye, RefreshCw, Copy, Check } from 'lucide-react'
import { getAllTestResults } from '../utils/api'

export default function TestResults() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [results, setResults] = useState([])
  const [filteredResults, setFilteredResults] = useState([])
  const [searchTerm, setSearchTerm] = useState(searchParams.get('test') || '')
  const [statusFilter, setStatusFilter] = useState(searchParams.get('status') || 'ALL')
  const [suiteFilter, setSuiteFilter] = useState('ALL')
  const [copiedId, setCopiedId] = useState(null)

  useEffect(() => {
    loadResults()
  }, [])

  useEffect(() => {
    filterResults()
  }, [searchTerm, statusFilter, suiteFilter, results])

  useEffect(() => {
    // Update URL params when filters change
    const params = new URLSearchParams()
    if (searchTerm) params.set('test', searchTerm)
    if (statusFilter !== 'ALL') params.set('status', statusFilter)
    if (suiteFilter !== 'ALL') params.set('suite', suiteFilter)
    setSearchParams(params)
  }, [searchTerm, statusFilter, suiteFilter])

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

  const handleCopyTestName = (testName) => {
    navigator.clipboard.writeText(testName)
    setCopiedId(testName)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const handleRerunTest = (testName) => {
    // In a real implementation, this would trigger a test run
    alert(`Rerunning test: ${testName}\n\nThis would trigger a test execution in a real implementation.`)
  }

  const handleViewDetails = (result) => {
    // Scroll to result and highlight it
    const element = document.getElementById(`test-${result.id || result.name}`)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' })
      element.classList.add('ring-4', 'ring-purple-500')
      setTimeout(() => {
        element.classList.remove('ring-4', 'ring-purple-500')
      }, 2000)
    }
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
      <div className="glass rounded-2xl p-4 flex gap-4 flex-wrap">
        <div className="flex-1 relative min-w-[200px]">
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
          className="px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 cursor-pointer"
        >
          <option value="ALL">All Statuses</option>
          <option value="PASSED">✅ Passed</option>
          <option value="FAILED">❌ Failed</option>
          <option value="SKIPPED">⏭️ Skipped</option>
        </select>
        <select
          value={suiteFilter}
          onChange={(e) => setSuiteFilter(e.target.value)}
          className="px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 cursor-pointer"
        >
          <option value="ALL">All Suites</option>
          <option value="SauceDemo">SauceDemo</option>
          <option value="BlazeDemo">BlazeDemo</option>
          <option value="OrangeHRM">OrangeHRM</option>
          <option value="API">API</option>
        </select>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={loadResults}
          className="px-4 py-2 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/50 rounded-lg flex items-center gap-2 transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Refresh</span>
        </motion.button>
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
              id={`test-${result.id || result.name}`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              whileHover={{ scale: 1.02, x: 5 }}
              className={`glass rounded-xl p-6 border-l-4 ${statusColors[result.status] || statusColors.PASSED} card-hover transition-all`}
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
                <div className="flex gap-2 ml-4">
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => handleViewDetails(result)}
                    className="p-2 rounded-lg bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/50 transition-colors"
                    title="View Details"
                  >
                    <Eye className="w-4 h-4 text-blue-300" />
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => handleCopyTestName(result.name)}
                    className="p-2 rounded-lg bg-green-500/20 hover:bg-green-500/30 border border-green-500/50 transition-colors"
                    title="Copy Test Name"
                  >
                    {copiedId === result.name ? (
                      <Check className="w-4 h-4 text-green-300" />
                    ) : (
                      <Copy className="w-4 h-4 text-green-300" />
                    )}
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => handleRerunTest(result.name)}
                    className="p-2 rounded-lg bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/50 transition-colors"
                    title="Rerun Test"
                  >
                    <RefreshCw className="w-4 h-4 text-purple-300" />
                  </motion.button>
                </div>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </motion.div>
  )
}
