import { useState, useEffect, useCallback } from 'react'
import { useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Search, Filter, Eye, RefreshCw, Copy, Check } from 'lucide-react'
import { getAllTestResults } from '../utils/api'
import toast from 'react-hot-toast'

export default function TestResults() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [results, setResults] = useState([])
  const [filteredResults, setFilteredResults] = useState([])
  const [searchTerm, setSearchTerm] = useState(searchParams.get('test') || '')
  const [statusFilter, setStatusFilter] = useState(searchParams.get('status') || 'ALL')
  const [suiteFilter, setSuiteFilter] = useState(searchParams.get('suite') || 'ALL')
  const [copiedId, setCopiedId] = useState(null)

  // Update filters when URL params change (e.g., when navigating from StatCard)
  useEffect(() => {
    const urlStatus = searchParams.get('status') || 'ALL'
    const urlTest = searchParams.get('test') || ''
    const urlSuite = searchParams.get('suite') || 'ALL'
    
    if (urlStatus !== statusFilter) {
      setStatusFilter(urlStatus)
    }
    if (urlTest !== searchTerm) {
      setSearchTerm(urlTest)
    }
    if (urlSuite !== suiteFilter) {
      setSuiteFilter(urlSuite)
    }
  }, [searchParams, statusFilter, searchTerm, suiteFilter])

  const loadResults = useCallback(async () => {
    try {
      const data = await getAllTestResults()
      // Validate data is an array
      if (Array.isArray(data)) {
        setResults(data)
      } else {
        console.warn('API returned non-array data:', data)
        setResults([])
      }
    } catch (error) {
      console.error('Failed to load test results:', error)
      setResults([]) // Set empty array on error
    }
  }, [])

  const filterResults = useCallback(() => {
    if (!results || results.length === 0) {
      setFilteredResults([])
      return
    }

    let filtered = [...results] // Create a copy to avoid mutating state

    if (searchTerm) {
      filtered = filtered.filter(r => {
        if (!r) return false
        const name = (r.name || '').toLowerCase()
        const suite = (r.suite || '').toLowerCase()
        const search = searchTerm.toLowerCase()
        return name.includes(search) || suite.includes(search)
      })
    }

    if (statusFilter !== 'ALL') {
      filtered = filtered.filter(r => {
        if (!r || !r.status) return false
        const testStatus = (r.status || '').toUpperCase()
        const filterStatus = statusFilter.toUpperCase()
        return testStatus === filterStatus
      })
    }

    if (suiteFilter !== 'ALL') {
      filtered = filtered.filter(r => {
        if (!r || !r.suite) return false
        const testSuite = (r.suite || '').toUpperCase()
        const filterSuite = suiteFilter.toUpperCase()
        return testSuite === filterSuite
      })
    }

    setFilteredResults(filtered)
  }, [results, searchTerm, statusFilter, suiteFilter])

  // Load results on mount
  useEffect(() => {
    loadResults()
  }, [loadResults])

  // Filter results whenever filters or results change
  useEffect(() => {
    filterResults()
  }, [filterResults])

  // Update URL params when filters change (but don't trigger navigation)
  useEffect(() => {
    const params = new URLSearchParams()
    if (searchTerm) params.set('test', searchTerm)
    if (statusFilter !== 'ALL') params.set('status', statusFilter)
    if (suiteFilter !== 'ALL') params.set('suite', suiteFilter)
    
    // Only update if params actually changed to avoid infinite loops
    const currentParams = searchParams.toString()
    const newParams = params.toString()
    if (currentParams !== newParams) {
      setSearchParams(params, { replace: true })
    }
  }, [searchTerm, statusFilter, suiteFilter, searchParams, setSearchParams])

  const handleCopyTestName = async (testName) => {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(testName)
        setCopiedId(testName)
        toast.success(`✅ Copied: ${testName}`, {
          duration: 2000,
          icon: '📋',
        })
        setTimeout(() => setCopiedId(null), 2000)
      } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea')
        textArea.value = testName
        textArea.style.position = 'fixed'
        textArea.style.left = '-999999px'
        document.body.appendChild(textArea)
        textArea.select()
        document.execCommand('copy')
        document.body.removeChild(textArea)
        setCopiedId(testName)
        toast.success(`✅ Copied: ${testName}`, {
          duration: 2000,
          icon: '📋',
        })
        setTimeout(() => setCopiedId(null), 2000)
      }
    } catch (error) {
      console.error('Failed to copy:', error)
      toast.error('❌ Failed to copy test name', {
        duration: 2000,
      })
    }
  }

  const handleRerunTest = (testName, result) => {
    // Show confirmation dialog
    if (window.confirm(`Rerun test: ${testName}?\n\nThis will trigger a test execution.`)) {
      toast.loading(`🔄 Rerunning test: ${testName}...`, {
        duration: 2000,
      })
      
      // Simulate test execution (in real implementation, this would call an API)
      setTimeout(() => {
        toast.success(`✅ Test execution started: ${testName}`, {
          duration: 3000,
        })
        // Optionally reload results after a delay
        setTimeout(() => {
          loadResults()
        }, 3000)
      }, 2000)
    }
  }

  const handleViewDetails = (result) => {
    try {
      // Create a detailed view modal or expand the card
      const details = [
        `Test Name: ${result.name}`,
        `Suite: ${result.suite || 'Unknown'}`,
        `Status: ${result.status}`,
        `Duration: ${result.duration || 'N/A'}`,
        `Timestamp: ${new Date(result.timestamp || Date.now()).toLocaleString()}`,
        result.error ? `Error: ${result.error}` : 'No errors',
      ].join('\n')
      
      // Show details in a modal-like alert (in production, use a proper modal component)
      toast(
        (t) => (
          <div className="text-left">
            <div className="font-bold mb-2">📋 Test Details</div>
            <div className="text-sm space-y-1">
              <div><strong>Name:</strong> {result.name}</div>
              <div><strong>Suite:</strong> {result.suite || 'Unknown'}</div>
              <div><strong>Status:</strong> {result.status}</div>
              <div><strong>Duration:</strong> {result.duration || 'N/A'}</div>
              {result.error && (
                <div className="mt-2 text-red-300">
                  <strong>Error:</strong> {result.error}
                </div>
              )}
            </div>
          </div>
        ),
        {
          duration: 5000,
          icon: '👁️',
        }
      )
      
      // Also scroll to and highlight the element
      const elementId = `test-${result.id || result.name?.replace(/\s+/g, '-')}`
      const element = document.getElementById(elementId)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' })
        // Add highlight effect
        element.style.transition = 'all 0.3s ease'
        element.style.boxShadow = '0 0 20px rgba(168, 85, 247, 0.8)'
        setTimeout(() => {
          element.style.boxShadow = ''
        }, 2000)
      }
    } catch (error) {
      console.error('Error viewing details:', error)
      toast.error('❌ Failed to view details', {
        duration: 2000,
      })
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
              id={`test-${result.id || result.name?.replace(/\s+/g, '-') || `test-${index}`}`}
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
                    onClick={(e) => {
                      e.stopPropagation()
                      handleViewDetails(result)
                    }}
                    className="p-2 rounded-lg bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/50 transition-colors cursor-pointer"
                    title="View Details"
                  >
                    <Eye className="w-4 h-4 text-blue-300" />
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={(e) => {
                      e.stopPropagation()
                      handleCopyTestName(result.name)
                    }}
                    className="p-2 rounded-lg bg-green-500/20 hover:bg-green-500/30 border border-green-500/50 transition-colors cursor-pointer"
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
                    onClick={(e) => {
                      e.stopPropagation()
                      handleRerunTest(result.name, result)
                    }}
                    className="p-2 rounded-lg bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/50 transition-colors cursor-pointer"
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
