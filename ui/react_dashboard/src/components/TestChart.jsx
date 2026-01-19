import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = ['#10b981', '#ef4444', '#f59e0b', '#6366f1']

export function TestResultsBarChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
        <XAxis dataKey="suite" stroke="#9ca3af" />
        <YAxis stroke="#9ca3af" />
        <Tooltip 
          contentStyle={{ 
            backgroundColor: 'rgba(0,0,0,0.8)', 
            border: '1px solid rgba(255,255,255,0.2)',
            borderRadius: '8px'
          }} 
        />
        <Legend />
        <Bar dataKey="passed" fill="#10b981" name="✅ Passed" />
        <Bar dataKey="failed" fill="#ef4444" name="❌ Failed" />
        <Bar dataKey="skipped" fill="#f59e0b" name="⏭️ Skipped" />
      </BarChart>
    </ResponsiveContainer>
  )
}

export function TestResultsPieChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
          outerRadius={100}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip 
          contentStyle={{ 
            backgroundColor: 'rgba(0,0,0,0.8)', 
            border: '1px solid rgba(255,255,255,0.2)',
            borderRadius: '8px'
          }} 
        />
      </PieChart>
    </ResponsiveContainer>
  )
}
