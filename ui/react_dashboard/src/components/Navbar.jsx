import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { TestTube, BarChart3, History, Settings } from 'lucide-react'

export default function Navbar() {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: BarChart3, emoji: '📊' },
    { path: '/results', label: 'Test Results', icon: TestTube, emoji: '🧪' },
    { path: '/history', label: 'History', icon: History, emoji: '📜' },
    { path: '/settings', label: 'Settings', icon: Settings, emoji: '⚙️' },
  ]

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="glass border-b border-white/20 sticky top-0 z-50"
    >
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <motion.div
            whileHover={{ scale: 1.1, rotate: 5 }}
            className="flex items-center gap-2 text-2xl font-bold"
          >
            <span className="text-3xl">🧪</span>
            <span>Automation Testing Dashboard</span>
          </motion.div>

          <div className="flex gap-2">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              
              return (
                <Link key={item.path} to={item.path}>
                  <motion.div
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className={`
                      flex items-center gap-2 px-4 py-2 rounded-lg transition-all
                      ${isActive 
                        ? 'bg-purple-500/30 text-purple-200 border border-purple-400/50' 
                        : 'hover:bg-white/10 text-gray-300'
                      }
                    `}
                  >
                    <Icon size={18} />
                    <span className="hidden md:inline">{item.label}</span>
                    <span className="md:hidden">{item.emoji}</span>
                  </motion.div>
                </Link>
              )
            })}
          </div>
        </div>
      </div>
    </motion.nav>
  )
}
