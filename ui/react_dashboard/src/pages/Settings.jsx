import { motion } from 'framer-motion'
import { Settings as SettingsIcon, RefreshCw, Bell, Palette } from 'lucide-react'

export default function Settings() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <h1 className="text-4xl font-bold flex items-center gap-3">
        <span className="animate-pulse">⚙️</span> Settings
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div
          whileHover={{ scale: 1.02 }}
          className="glass rounded-xl p-6 card-hover"
        >
          <div className="flex items-center gap-3 mb-4">
            <RefreshCw className="w-6 h-6 text-purple-400" />
            <h2 className="text-xl font-bold">Auto Refresh</h2>
          </div>
          <p className="text-gray-400 mb-4">
            Automatically refresh dashboard data every 5 seconds
          </p>
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" defaultChecked className="w-4 h-4" />
            <span>Enable auto-refresh</span>
          </label>
        </motion.div>

        <motion.div
          whileHover={{ scale: 1.02 }}
          className="glass rounded-xl p-6 card-hover"
        >
          <div className="flex items-center gap-3 mb-4">
            <Bell className="w-6 h-6 text-purple-400" />
            <h2 className="text-xl font-bold">Notifications</h2>
          </div>
          <p className="text-gray-400 mb-4">
            Get notified when tests fail or complete
          </p>
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" defaultChecked className="w-4 h-4" />
            <span>Enable notifications</span>
          </label>
        </motion.div>

        <motion.div
          whileHover={{ scale: 1.02 }}
          className="glass rounded-xl p-6 card-hover"
        >
          <div className="flex items-center gap-3 mb-4">
            <Palette className="w-6 h-6 text-purple-400" />
            <h2 className="text-xl font-bold">Theme</h2>
          </div>
          <p className="text-gray-400 mb-4">
            Choose your preferred color scheme
          </p>
          <select className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500">
            <option>Dark (Default)</option>
            <option>Light</option>
            <option>Auto</option>
          </select>
        </motion.div>

        <motion.div
          whileHover={{ scale: 1.02 }}
          className="glass rounded-xl p-6 card-hover"
        >
          <div className="flex items-center gap-3 mb-4">
            <SettingsIcon className="w-6 h-6 text-purple-400" />
            <h2 className="text-xl font-bold">API Configuration</h2>
          </div>
          <p className="text-gray-400 mb-4">
            Configure API endpoint settings
          </p>
          <input
            type="text"
            placeholder="http://localhost:5001/api"
            defaultValue="http://localhost:5001/api"
            className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </motion.div>
      </div>
    </motion.div>
  )
}
