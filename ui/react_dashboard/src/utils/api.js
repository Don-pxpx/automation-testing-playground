import axios from 'axios'

// In Docker, use the service name. In local dev, use localhost
const API_BASE_URL = import.meta.env.VITE_API_URL ||
  (window.location.hostname === 'localhost' ? 'http://localhost:5001/api' : '/api')

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getDashboardStats = async () => {
  try {
    const response = await api.get('/dashboard/stats')
    return response.data
  } catch (error) {
    // Return mock data if API is not available
    return {
      totalTests: 42,
      passed: 35,
      failed: 5,
      skipped: 2,
      passRate: 83.3,
      totalSuites: 4,
      lastRun: new Date().toISOString(),
    }
  }
}

export const getRecentTestResults = async (limit = 10) => {
  try {
    const response = await api.get(`/test-results/recent?limit=${limit}`)
    return response.data
  } catch (error) {
    // Return mock data
    return []
  }
}

export const getAllTestResults = async () => {
  try {
    const response = await api.get('/test-results')
    return response.data
  } catch (error) {
    return []
  }
}

export const getTestHistory = async () => {
  try {
    const response = await api.get('/test-history')
    return response.data
  } catch (error) {
    return []
  }
}

export const getTestExecutionDetail = async (id) => {
  try {
    const response = await api.get(`/test-executions/${id}`)
    return response.data
  } catch (error) {
    console.error('Failed to fetch test execution detail:', error)
    throw error
  }
}

export default api
