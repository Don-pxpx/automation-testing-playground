import time
import traceback
import sys
from prettytable import PrettyTable
from datetime import datetime

class InlineLogger:
    def __init__(self):
        self.step_counter = 1
        self.start_time = time.time()
        self._last_step_started_at = None
        self.errors = []
        self.warnings = []
        self.steps = []

    def step(self, description: str):
        self._last_step_started_at = time.time()
        step_info = {
            'number': self.step_counter,
            'description': description,
            'start_time': self._last_step_started_at,
            'status': 'running'
        }
        self.steps.append(step_info)
        print(f"\n🔵🔷🔹 ➡️ STEP {self.step_counter}: {description.upper()} 🔹🔷🔵")
        self.step_counter += 1

    def note(self, message: str):
        print(f"🗒️ ✍️ NOTE: {message}")

    def success(self, message: str):
        if self.steps:
            self.steps[-1]['status'] = 'success'
            self.steps[-1]['end_time'] = time.time()
        print(f"✅✨ SUCCESS: {message}")

    def warning(self, message: str):
        warning_info = {
            'message': message,
            'timestamp': time.time(),
            'step': self.step_counter - 1 if self.steps else 0
        }
        self.warnings.append(warning_info)
        print(f"⚠️🚧 WARNING: {message}")

    def error(self, message: str, exception=None):
        error_info = {
            'message': message,
            'timestamp': time.time(),
            'step': self.step_counter - 1 if self.steps else 0,
            'exception': exception,
            'traceback': traceback.format_exc() if exception else None
        }
        self.errors.append(error_info)
        
        if self.steps:
            self.steps[-1]['status'] = 'failed'
            self.steps[-1]['end_time'] = time.time()
        
        print(f"🛑❌ ERROR: {message}")
        if exception:
            print(f"🔍 Exception Type: {type(exception).__name__}")
            print(f"🔍 Exception Message: {str(exception)}")

    def highlight(self, message: str):
        print(f"🌟💡 HIGHLIGHT: {message}")

    def divider(self):
        print("\n" + "═" * 80 + "\n")

    def test_start(self, test_name: str):
        print(f"\n🚀 STARTING TEST: {test_name}")
        print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def test_end(self, test_name: str, status: str):
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        duration = time.time() - self.start_time
        
        status_emoji = {
            'passed': '✅',
            'failed': '❌',
            'skipped': '⏭️',
            'error': '💥'
        }.get(status, '❓')
        
        print(f"\n{status_emoji} TEST COMPLETED: {test_name}")
        print(f"⏰ End Time: {end_time}")
        print(f"⏱️ Duration: {duration:.2f} seconds")

    def summary(self, passed: int, failed: int, skipped: int):
        total_time = time.time() - self.start_time
        self.divider()
        print("📊✨ FINAL TEST EXECUTION SUMMARY ✨📊")

        # Main summary table
        table = PrettyTable()
        table.field_names = ["🏁 RESULT", "✅ PASSED", "❌ FAILED", "⏭️ SKIPPED", "⏱️ TOTAL TIME (s)"]
        table.add_row(["📋 SUMMARY", passed, failed, skipped, f"{total_time:.2f}"])
        print(table.get_string())

        # Step-by-step breakdown
        if self.steps:
            print(f"\n📋 STEP-BY-STEP BREAKDOWN:")
            step_table = PrettyTable()
            step_table.field_names = ["STEP", "DESCRIPTION", "STATUS", "DURATION (s)"]
            
            for step in self.steps:
                duration = step.get('end_time', time.time()) - step['start_time']
                status_emoji = {
                    'running': '🔄',
                    'success': '✅',
                    'failed': '❌'
                }.get(step['status'], '❓')
                
                step_table.add_row([
                    step['number'],
                    step['description'][:30] + "..." if len(step['description']) > 30 else step['description'],
                    f"{status_emoji} {step['status'].upper()}",
                    f"{duration:.2f}"
                ])
            print(step_table.get_string())

        # Error details
        if self.errors:
            print(f"\n🚨 ERROR DETAILS ({len(self.errors)} errors):")
            for i, error in enumerate(self.errors, 1):
                print(f"\n❌ ERROR {i}:")
                print(f"   📝 Message: {error['message']}")
                print(f"   🔢 Step: {error['step']}")
                if error['exception']:
                    print(f"   🔍 Type: {type(error['exception']).__name__}")
                    print(f"   🔍 Details: {str(error['exception'])}")
                if error['traceback']:
                    print(f"   📍 Traceback:")
                    for line in error['traceback'].split('\n')[-5:]:  # Last 5 lines
                        if line.strip():
                            print(f"      {line}")

        # Warning details
        if self.warnings:
            print(f"\n⚠️ WARNING DETAILS ({len(self.warnings)} warnings):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning['message']}")

        # Final status
        if failed > 0:
            print(f"\n🚨 {failed} TEST(S) FAILED - IMMEDIATE ATTENTION REQUIRED!")
            print("🔍 Check the error details above for troubleshooting.")
        elif skipped > 0:
            print(f"\n⚠️ {skipped} TEST(S) SKIPPED - Review test coverage.")
        else:
            print(f"\n🎉 ALL {passed} TESTS PASSED SUCCESSFULLY!")
            print("🌟 Excellent work! All automation tests are green.")
        
        self.divider()

    def capture_exception(self, exception):
        """Capture exception details for detailed error reporting"""
        return {
            'type': type(exception).__name__,
            'message': str(exception),
            'traceback': traceback.format_exc(),
            'line_number': traceback.extract_tb(sys.exc_info()[2])[-1].lineno if sys.exc_info()[2] else None
        }
