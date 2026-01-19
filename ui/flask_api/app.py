from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Path to reports directory
BASE_DIR = Path(__file__).parent.parent.parent
REPORTS_DIR = BASE_DIR / 'reports'

def load_test_results_from_reports():
    """Load test results from HTML reports and generate JSON data"""
    results = []
    
    # Parse HTML reports if they exist
    if REPORTS_DIR.exists():
        for html_file in REPORTS_DIR.glob('*.html'):
            try:
                # For now, generate mock data based on file names
                # In production, you'd parse the HTML or use pytest-html JSON output
                suite_name = html_file.stem.replace('_report', '').replace('_', ' ').title()
                results.append({
                    'id': len(results) + 1,
                    'name': f'Test Suite: {suite_name}',
                    'suite': suite_name,
                    'status': 'PASSED',
                    'duration': '12.5s',
                    'timestamp': datetime.now().isoformat(),
                })
            except Exception as e:
                print(f"Error loading {html_file}: {e}")
    
    return results

def load_test_executions():
    """Load test execution history"""
    executions = []
    executions_file = REPORTS_DIR / 'test-executions.json'
    
    if executions_file.exists():
        try:
            with open(executions_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    executions.extend(data)
                elif isinstance(data, dict):
                    executions.append(data)
        except Exception as e:
            print(f"Error loading test executions: {e}")
    
    return executions

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': '🧪 Automation Testing Dashboard API is running!',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    results = load_test_results_from_reports()
    
    # Calculate stats
    total_tests = len(results) * 10  # Mock: assume 10 tests per suite
    passed = int(total_tests * 0.85)
    failed = int(total_tests * 0.10)
    skipped = int(total_tests * 0.05)
    pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    
    return jsonify({
        'totalTests': total_tests or 42,
        'passed': passed or 35,
        'failed': failed or 5,
        'skipped': skipped or 2,
        'passRate': pass_rate or 83.3,
        'totalSuites': len(results) or 4,
        'lastRun': datetime.now().isoformat()
    })

@app.route('/api/test-results/recent', methods=['GET'])
def get_recent_test_results():
    """Get recent test results"""
    limit = request.args.get('limit', 10, type=int)
    results = load_test_results_from_reports()
    
    # Sort by timestamp (most recent first)
    results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # If no results, return mock data
    if not results:
        results = [
            {
                'id': 1,
                'name': 'Login Test - Valid Credentials',
                'suite': 'SauceDemo',
                'status': 'PASSED',
                'duration': '2.3s',
                'timestamp': datetime.now().isoformat(),
            },
            {
                'id': 2,
                'name': 'Cart Operations Test',
                'suite': 'SauceDemo',
                'status': 'PASSED',
                'duration': '3.1s',
                'timestamp': (datetime.now() - timedelta(minutes=5)).isoformat(),
            },
            {
                'id': 3,
                'name': 'Flight Booking Test',
                'suite': 'BlazeDemo',
                'status': 'FAILED',
                'duration': '5.2s',
                'timestamp': (datetime.now() - timedelta(minutes=10)).isoformat(),
                'error': 'Element not found: booking confirmation'
            },
        ]
    
    return jsonify(results[:limit])

@app.route('/api/test-results', methods=['GET'])
def get_all_test_results():
    """Get all test results"""
    results = load_test_results_from_reports()
    
    if not results:
        # Return mock data
        results = [
            {
                'id': i,
                'name': f'Test Case {i}',
                'suite': ['SauceDemo', 'BlazeDemo', 'OrangeHRM', 'API'][i % 4],
                'status': ['PASSED', 'PASSED', 'FAILED', 'SKIPPED'][i % 4],
                'duration': f'{2 + i * 0.5:.1f}s',
                'timestamp': (datetime.now() - timedelta(minutes=i * 5)).isoformat(),
            }
            for i in range(1, 21)
        ]
    
    return jsonify(results)

@app.route('/api/test-history', methods=['GET'])
def get_test_history():
    """Get test execution history"""
    executions = load_test_executions()
    
    if not executions:
        # Return mock data
        executions = [
            {
                'id': 1,
                'suite': 'SauceDemo Test Suite',
                'status': 'SUCCESS',
                'totalTests': 15,
                'passed': 14,
                'failed': 1,
                'skipped': 0,
                'duration': '45.2s',
                'timestamp': (datetime.now() - timedelta(minutes=30)).isoformat(),
            },
            {
                'id': 2,
                'suite': 'BlazeDemo Test Suite',
                'status': 'SUCCESS',
                'totalTests': 8,
                'passed': 8,
                'failed': 0,
                'skipped': 0,
                'duration': '32.1s',
                'timestamp': (datetime.now() - timedelta(minutes=25)).isoformat(),
            },
            {
                'id': 3,
                'suite': 'OrangeHRM Test Suite',
                'status': 'FAILED',
                'totalTests': 12,
                'passed': 10,
                'failed': 2,
                'skipped': 0,
                'duration': '58.7s',
                'timestamp': (datetime.now() - timedelta(minutes=20)).isoformat(),
            },
        ]
    
    return jsonify(executions)

if __name__ == '__main__':
    print('🚀 Starting Automation Testing Dashboard API...')
    print('📡 API will be available at http://localhost:5001')
    print('🎯 React dashboard should connect automatically!')
    app.run(debug=True, port=5001, host='0.0.0.0')
