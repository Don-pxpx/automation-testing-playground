#!/usr/bin/env python3
"""
CLI tool for running Performance & Security Testing Lab tests
Provides easy access to different testing scenarios
"""

import argparse
import sys
import subprocess
from typing import Optional

from automation_testing_playground.helpers.logger import PerformanceSecurityLogger
from automation_testing_playground.config.settings import TEST_TARGETS_CONFIG

# Initialize logger
logger = PerformanceSecurityLogger("CLI")


def run_performance_tests(test_type: str = "all", target: Optional[str] = None):
    """Run performance tests"""
    logger.start_test("Performance Test Suite", "performance")
    
    try:
        if test_type == "api":
            logger.step("Running API performance tests")
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "tests/integration/api/test_api_performance.py", 
                "-v", "-s", "-m", "performance"
            ], capture_output=True, text=True)
        elif test_type == "load":
            logger.step("Running load tests with Locust")
            if target:
                result = subprocess.run([
                    sys.executable, "-m", "locust",
                    "-f", "src/automation_testing_playground/performance/load_testing/locustfile.py",
                    "--host", target,
                    "--users", "10",
                    "--spawn-rate", "2",
                    "--run-time", "60s",
                    "--headless"
                ], capture_output=True, text=True)
            else:
                logger.error("Target URL required for load tests")
                return False
        else:
            logger.step("Running all performance tests")
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "tests/integration/", 
                "-v", "-s", "-m", "performance"
            ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.success("Performance tests completed successfully")
            print(result.stdout)
            return True
        else:
            logger.error("Performance tests failed")
            print(result.stderr)
            return False
    
    except Exception as e:
        logger.error("Failed to run performance tests", e)
        return False
    
    finally:
        logger.end_test("Performance Test Suite")


def run_security_tests(test_type: str = "all", target: Optional[str] = None):
    """Run security tests"""
    logger.start_test("Security Test Suite", "security")
    
    try:
        if test_type == "scan":
            logger.step("Running security vulnerability scan")
            from automation_testing_playground.security.vulnerability_scan.security_scanner import run_security_scan
            
            if target:
                results = run_security_scan(target)
            else:
                logger.info("No target specified, scanning all configured targets")
                from automation_testing_playground.security.vulnerability_scan.security_scanner import scan_all_targets
                results = scan_all_targets()
            
            logger.success("Security scan completed")
            return True
        
        elif test_type == "auth":
            logger.step("Running authentication security tests")
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "tests/security/", 
                "-v", "-s", "-m", "security"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.success("Authentication security tests completed")
                print(result.stdout)
                return True
            else:
                logger.error("Authentication security tests failed")
                print(result.stderr)
                return False
        
        else:
            logger.step("Running all security tests")
            # Run security scanner
            from automation_testing_playground.security.vulnerability_scan.security_scanner import scan_all_targets
            scan_results = scan_all_targets()
            
            # Run security test files
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "tests/security/", 
                "-v", "-s", "-m", "security"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.success("All security tests completed")
                print(result.stdout)
                return True
            else:
                logger.error("Security tests failed")
                print(result.stderr)
                return False
    
    except Exception as e:
        logger.error("Failed to run security tests", e)
        return False
    
    finally:
        logger.end_test("Security Test Suite")


def run_integration_tests():
    """Run integration tests"""
    logger.start_test("Integration Test Suite", "integration")
    
    try:
        logger.step("Running integration tests")
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/integration/", 
            "-v", "-s", "-m", "integration"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.success("Integration tests completed successfully")
            print(result.stdout)
            return True
        else:
            logger.error("Integration tests failed")
            print(result.stderr)
            return False
    
    except Exception as e:
        logger.error("Failed to run integration tests", e)
        return False
    
    finally:
        logger.end_test("Integration Test Suite")


def list_targets():
    """List available test targets"""
    logger.info("Available test targets:")
    
    print("\n🌐 Demo Applications:")
    for name, url in TEST_TARGETS_CONFIG.DEMO_APPS.items():
        print(f"  • {name}: {url}")
    
    print("\n🔌 API Endpoints:")
    for name, url in TEST_TARGETS_CONFIG.API_ENDPOINTS.items():
        print(f"  • {name}: {url}")
    
    print("\n🏠 Internal Applications:")
    for name, url in TEST_TARGETS_CONFIG.INTERNAL_APPS.items():
        print(f"  • {name}: {url}")


def run_locust_load_test(target: str, users: int = 10, spawn_rate: float = 2, run_time: str = "60s"):
    """Run Locust load test"""
    logger.start_test("Locust Load Test", "performance")
    
    try:
        logger.step(f"Starting Locust load test for {target}")
        logger.info(f"Configuration: {users} users, {spawn_rate} spawn rate, {run_time} duration")
        
        result = subprocess.run([
            sys.executable, "-m", "locust",
            "-f", "src/automation_testing_playground/performance/load_testing/locustfile.py",
            "--host", target,
            "--users", str(users),
            "--spawn-rate", str(spawn_rate),
            "--run-time", run_time,
            "--headless"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.success("Locust load test completed successfully")
            print(result.stdout)
            return True
        else:
            logger.error("Locust load test failed")
            print(result.stderr)
            return False
    
    except Exception as e:
        logger.error("Failed to run Locust load test", e)
        return False
    
    finally:
        logger.end_test("Locust Load Test")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Performance & Security Testing Lab CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_tests.py performance api                    # Run API performance tests
  python scripts/run_tests.py performance load --target https://example.com  # Run load test
  python scripts/run_tests.py security scan --target https://example.com     # Run security scan
  python scripts/run_tests.py security auth                     # Run authentication tests
  python scripts/run_tests.py integration                       # Run integration tests
  python scripts/run_tests.py locust --target https://example.com --users 50  # Run Locust test
  python scripts/run_tests.py targets                           # List available targets
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Performance tests
    perf_parser = subparsers.add_parser("performance", help="Run performance tests")
    perf_parser.add_argument("type", choices=["all", "api", "load"], 
                           help="Type of performance test to run")
    perf_parser.add_argument("--target", help="Target URL for load tests")
    
    # Security tests
    sec_parser = subparsers.add_parser("security", help="Run security tests")
    sec_parser.add_argument("type", choices=["all", "scan", "auth"], 
                          help="Type of security test to run")
    sec_parser.add_argument("--target", help="Target URL for security scan")
    
    # Integration tests
    subparsers.add_parser("integration", help="Run integration tests")
    
    # Locust load test
    locust_parser = subparsers.add_parser("locust", help="Run Locust load test")
    locust_parser.add_argument("--target", required=True, help="Target URL")
    locust_parser.add_argument("--users", type=int, default=10, help="Number of users")
    locust_parser.add_argument("--spawn-rate", type=float, default=2, help="Spawn rate")
    locust_parser.add_argument("--run-time", default="60s", help="Test duration")
    
    # List targets
    subparsers.add_parser("targets", help="List available test targets")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute commands
    if args.command == "performance":
        success = run_performance_tests(args.type, args.target)
        sys.exit(0 if success else 1)
    
    elif args.command == "security":
        success = run_security_tests(args.type, args.target)
        sys.exit(0 if success else 1)
    
    elif args.command == "integration":
        success = run_integration_tests()
        sys.exit(0 if success else 1)
    
    elif args.command == "locust":
        success = run_locust_load_test(args.target, args.users, args.spawn_rate, args.run_time)
        sys.exit(0 if success else 1)
    
    elif args.command == "targets":
        list_targets()
        sys.exit(0)


if __name__ == "__main__":
    main()
