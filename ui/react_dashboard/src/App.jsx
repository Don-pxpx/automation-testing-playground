import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Toaster } from 'react-hot-toast'
import ErrorBoundary from './components/ErrorBoundary'
import Dashboard from './pages/Dashboard'
import TestResults from './pages/TestResults'
import TestHistory from './pages/TestHistory'
import Settings from './pages/Settings'
import Navbar from './components/Navbar'

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <div className="min-h-screen">
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 3000,
              style: {
                background: '#1a1a2e',
                color: '#fff',
                border: '1px solid rgba(168, 85, 247, 0.5)',
              },
              success: {
                iconTheme: {
                  primary: '#10b981',
                  secondary: '#fff',
                },
              },
              error: {
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#fff',
                },
              },
            }}
          />
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
    </ErrorBoundary>
  )
}

export default App
