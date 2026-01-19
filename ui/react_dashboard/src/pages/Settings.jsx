import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Settings as SettingsIcon, RefreshCw, Bell, Palette, Save, Check } from 'lucide-react'

export default function Settings() {
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [notifications, setNotifications] = useState(true)
  const [theme, setTheme] = useState('dark')
  const [apiUrl, setApiUrl] = useState('http://localhost:5001/api')
  const [saved, setSaved] = useState(false)
  const timeoutRef = useRef(null)

  useEffect(() => {
    // Load saved settings from localStorage
    const savedAutoRefresh = localStorage.getItem('autoRefresh')
    const savedNotifications = localStorage.getItem('notifications')
    const savedTheme = localStorage.getItem('theme')
    const savedApiUrl = localStorage.getItem('apiUrl')

    if (savedAutoRefresh !== null) setAutoRefresh(savedAutoRefresh === 'true')
    if (savedNotifications !== null) setNotifications(savedNotifications === 'true')
    if (savedTheme) setTheme(savedTheme)
    if (savedApiUrl) setApiUrl(savedApiUrl)

    // Cleanup timeout on unmount
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [])

  const handleSave = () => {
    localStorage.setItem('autoRefresh', autoRefresh.toString())
    localStorage.setItem('notifications', notifications.toString())
    localStorage.setItem('theme', theme)
    localStorage.setItem('apiUrl', apiUrl)
    setSaved(true)
    
    // Clear existing timeout if any
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
    }
    
    // Set new timeout
    timeoutRef.current = setTimeout(() => setSaved(false), 2000)
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-4xl font-bold flex items-center gap-3">
          <span className="animate-pulse">⚙️</span> Settings
        </h1>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSave}
          className="px-6 py-3 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/50 rounded-lg flex items-center gap-2 transition-colors"
        >
          {saved ? (
            <>
              <Check className="w-5 h-5" />
              <span>Saved!</span>
            </>
          ) : (
            <>
              <Save className="w-5 h-5" />
              <span>Save Settings</span>
            </>
          )}
        </motion.button>
      </div>

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
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="w-4 h-4 cursor-pointer"
            />
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
            <input
              type="checkbox"
              checked={notifications}
              onChange={(e) => setNotifications(e.target.checked)}
              className="w-4 h-4 cursor-pointer"
            />
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
          <select
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 cursor-pointer"
          >
            <option value="dark">Dark (Default)</option>
            <option value="light">Light</option>
            <option value="auto">Auto</option>
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
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
            className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </motion.div>
      </div>
    </motion.div>
  )
}
