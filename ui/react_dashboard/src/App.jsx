import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import Dashboard from './pages/Dashboard'
import TestResults from './pages/TestResults'
import TestHistory from './pages/TestHistory'
import Settings from './pages/Settings'
import Navbar from './components/Navbar'

function App() {
  return (
    <Router>
      <div className="min-h-screen">
        <Navbar />
        <motion.main
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="container mx-auto px-4 py-8"
        >
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/results" element={<TestResults />} />
            <Route path="/history" element={<TestHistory />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </motion.main>
      </div>
    </Router>
  )
}

export default App
