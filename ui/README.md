# 🧪 Automation Testing Dashboard

A fun, animated React dashboard for visualizing automation test results with emojis, charts, and real-time updates!

## 🎯 Features

- **📊 Real-time Dashboard** - Live test statistics and metrics
- **🧪 Test Results** - Detailed view of all test executions
- **📜 Test History** - Historical test run data
- **⚙️ Settings** - Customize dashboard preferences
- **🎨 Beautiful UI** - Animated, emoji-rich interface with Tailwind CSS
- **📈 Charts** - Visual representation of test results using Recharts

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+ (for Flask API)
- pip

### Installation

1. **Install React Dashboard dependencies:**
```bash
cd ui/react_dashboard
npm install
```

2. **Install Flask API dependencies:**
```bash
cd ../flask_api
pip install -r requirements.txt
```

### Running the Dashboard

**Option 1: Manual Start (Two Terminals)**

Terminal 1 - Start Flask API:
```bash
cd ui/flask_api
python app.py
```

Terminal 2 - Start React Dashboard:
```bash
cd ui/react_dashboard
npm run dev
```

**Option 2: Using Docker (Recommended)**

```bash
cd ui
docker-compose up
```

Then open your browser to:
- **React Dashboard:** http://localhost:3001
- **Flask API:** http://localhost:5001

## 📁 Structure

```
ui/
├── react_dashboard/          # React frontend
│   ├── src/
│   │   ├── pages/          # Dashboard pages
│   │   ├── components/     # Reusable components
│   │   └── utils/          # API utilities
│   └── package.json
├── flask_api/              # Flask backend
│   ├── app.py              # API server
│   └── requirements.txt
└── docker-compose.yml      # Docker orchestration
```

## 🎨 Pages

- **Dashboard** (`/`) - Overview with stats, charts, and recent tests
- **Test Results** (`/results`) - All test results with filtering
- **History** (`/history`) - Test execution history
- **Settings** (`/settings`) - Dashboard configuration

## 🔌 API Endpoints

- `GET /api/health` - Health check
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/test-results/recent?limit=10` - Recent test results
- `GET /api/test-results` - All test results
- `GET /api/test-history` - Test execution history

## 🛠️ Development

### React Dashboard
```bash
cd ui/react_dashboard
npm run dev      # Development server
npm run build    # Production build
npm run preview  # Preview production build
```

### Flask API
```bash
cd ui/flask_api
python app.py    # Development server (auto-reload)
```

## 📝 Notes

- The dashboard currently uses mock data when real test results aren't available
- To connect real test results, update the Flask API to parse your test report files
- The dashboard auto-refreshes every 5 seconds

## 🎉 Enjoy!

Have fun exploring your test results! 🧪✨
