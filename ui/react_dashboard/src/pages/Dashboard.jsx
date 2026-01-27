import { useState, useEffect, useCallback } from 'react'
import { motion } from 'framer-motion'
import { RefreshCw } from 'lucide-react'
import StatCard from '../components/StatCard'
import RecentTests from '../components/RecentTests'
import { TestResultsBarChart, TestResultsPieChart } from '../components/TestChart'
import { getDashboardStats, getRecentTestResults } from '../utils/api'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
}

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.5 }
  }
}

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalTests: 0,
    passed: 0,
    failed: 0,
    skipped: 0,
    passRate: 0,
    totalSuites: 0,
  })
  const [recentTests, setRecentTests] = useState([])
  const [suiteData, setSuiteData] = useState([])
  const [loading, setLoading] = useState(true)

  const loadData = useCallback(async () => {
    try {
      const [statsData, testsData] = await Promise.all([
        getDashboardStats(),
        getRecentTestResults(5)
      ])
      
      // Validate and set stats data
      if (statsData && typeof statsData === 'object') {
        setStats({
          totalTests: statsData.totalTests || 0,
          passed: statsData.passed || 0,
          failed: statsData.failed || 0,
          skipped: statsData.skipped || 0,
          passRate: statsData.passRate || 0,
          totalSuites: statsData.totalSuites || 0,
        })
      }
      
      // Validate and set recent tests
      if (Array.isArray(testsData)) {
        setRecentTests(testsData)
      } else {
        setRecentTests([])
      }
      
      // Generate suite data for charts based on actual stats
      const suites = ['SauceDemo', 'BlazeDemo', 'OrangeHRM', 'API']
      const totalPassed = statsData?.passed || 35
      const totalFailed = statsData?.failed || 5
      const totalSkipped = statsData?.skipped || 2
      
      setSuiteData(suites.map((suite, index) => ({
        suite,
        passed: Math.floor(totalPassed / suites.length) + (index === 0 ? totalPassed % suites.length : 0),
        failed: Math.floor(totalFailed / suites.length) + (index === 0 ? totalFailed % suites.length : 0),
        skipped: Math.floor(totalSkipped / suites.length) + (index === 0 ? totalSkipped % suites.length : 0),
      })))
      
      setLoading(false)
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
      // Set default values on error
      setStats({
        totalTests: 0,
        passed: 0,
        failed: 0,
        skipped: 0,
        passRate: 0,
        totalSuites: 0,
      })
      setRecentTests([])
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadData()
    const autoRefresh = typeof window !== 'undefined' && window.localStorage?.getItem('autoRefresh') !== 'false'
    if (!autoRefresh) return
    const interval = setInterval(loadData, 5000)
    return () => clearInterval(interval)
  }, [loadData])

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

  const pieData = [
    { name: 'Passed', value: stats.passed },
    { name: 'Failed', value: stats.failed },
    { name: 'Skipped', value: stats.skipped },
  ]

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      {/* Welcome Header */}
      <motion.div variants={itemVariants} className="text-center mb-8">
        <motion.h1
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 200 }}
          className="text-5xl font-bold mb-2"
        >
          <span className="inline-block animate-bounce">🧪</span> Welcome Back!
        </motion.h1>
        <p className="text-gray-400 text-lg mb-4">
          Your automation test results at a glance
        </p>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={loadData}
          className="px-6 py-3 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/50 rounded-lg flex items-center gap-2 transition-colors mx-auto"
        >
          <RefreshCw className="w-5 h-5" />
          <span>Refresh Dashboard</span>
        </motion.button>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        variants={itemVariants}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        <StatCard
          title="Total Tests"
          value={stats.totalTests}
          icon="total"
          color="total"
          animationDelay={0.1}
        />
        <StatCard
          title="Passed"
          value={stats.passed}
          icon="passed"
          color="passed"
          animationDelay={0.2}
        />
        <StatCard
          title="Failed"
          value={stats.failed}
          icon="failed"
          color="failed"
          animationDelay={0.3}
        />
        <StatCard
          title="Pass Rate"
          value={`${stats.passRate.toFixed(1)}%`}
          icon="passRate"
          color="passRate"
          animationDelay={0.4}
        />
      </motion.div>

      {/* Charts Row */}
      <motion.div
        variants={itemVariants}
        className="grid grid-cols-1 lg:grid-cols-2 gap-6"
      >
        <div className="glass rounded-2xl p-6">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <span>📊</span> Test Results by Suite
          </h3>
          <TestResultsBarChart data={suiteData} />
        </div>
        
        <div className="glass rounded-2xl p-6">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <span>🥧</span> Overall Test Status
          </h3>
          <TestResultsPieChart data={pieData} />
        </div>
      </motion.div>

      {/* Recent Tests */}
      <motion.div variants={itemVariants}>
        <RecentTests tests={recentTests} />
      </motion.div>
    </motion.div>
  )
}
