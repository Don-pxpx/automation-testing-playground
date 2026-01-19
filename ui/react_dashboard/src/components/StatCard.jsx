import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { CheckCircle, XCircle, SkipForward, TestTube, TrendingUp, Clock, ArrowRight } from 'lucide-react'

const iconMap = {
  total: TestTube,
  passed: CheckCircle,
  failed: XCircle,
  skipped: SkipForward,
  passRate: TrendingUp,
  suites: TestTube,
  lastRun: Clock,
}

const colorMap = {
  total: 'from-blue-500/20 to-blue-600/20 border-blue-500/30',
  passed: 'from-green-500/20 to-green-600/20 border-green-500/30',
  failed: 'from-red-500/20 to-red-600/20 border-red-500/30',
  skipped: 'from-yellow-500/20 to-yellow-600/20 border-yellow-500/30',
  passRate: 'from-purple-500/20 to-purple-600/20 border-purple-500/30',
  suites: 'from-indigo-500/20 to-indigo-600/20 border-indigo-500/30',
  lastRun: 'from-cyan-500/20 to-cyan-600/20 border-cyan-500/30',
}

const StatCard = ({ title, value, icon, color, animationDelay = 0, onClick }) => {
  const navigate = useNavigate()
  const IconComponent = iconMap[icon] || TestTube
  const colorClass = colorMap[color] || colorMap.total

  const handleClick = () => {
    if (onClick) {
      onClick()
    } else {
      // Default behavior: navigate to results with filter
      const statusMap = {
        'Total Tests': 'ALL',
        'Passed': 'PASSED',
        'Failed': 'FAILED',
        'Skipped': 'SKIPPED',
        'Pass Rate': 'ALL',
      }
      const status = statusMap[title] || 'ALL'
      navigate(`/results?status=${status}`)
    }
  }

  return (
    <motion.div
      className={`relative p-6 rounded-2xl shadow-xl backdrop-blur-md border ${colorClass} overflow-hidden cursor-pointer group`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: animationDelay, duration: 0.5 }}
      whileHover={{ scale: 1.03, boxShadow: "0 10px 20px rgba(0,0,0,0.2)" }}
      whileTap={{ scale: 0.98 }}
      onClick={handleClick}
    >
      <motion.div
        className="absolute -top-4 -right-4 text-6xl opacity-10"
        animate={{
          y: [0, -10, 0],
          rotate: [0, 10, -10, 0],
        }}
        transition={{
          duration: 5,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      >
        <IconComponent size={64} />
      </motion.div>
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-200 mb-2">{title}</h3>
          <p className="text-4xl font-bold text-white">
            {value}
          </p>
        </div>
        <motion.div
          className="opacity-0 group-hover:opacity-100 transition-opacity"
          animate={{ x: [0, 5, 0] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          <ArrowRight className="w-6 h-6 text-white/60" />
        </motion.div>
      </div>
    </motion.div>
  )
}

export default StatCard
