import time
from prettytable import PrettyTable

class InlineLogger:
    def __init__(self):
        self.step_counter = 1
        self.start_time = time.time()
        self._last_step_started_at = None

    def step(self, description: str):
        self._last_step_started_at = time.time()
        print(f"\n🔵🔷🔹 ➡️ STEP {self.step_counter}: {description.upper()} 🔹🔷🔵")
        self.step_counter += 1

    def note(self, message: str):
        print(f"🗒️ ✍️ NOTE: {message}")

    def success(self, message: str):
        print(f"✅✨ SUCCESS: {message}")

    def warning(self, message: str):
        print(f"⚠️🚧 WARNING: {message}")

    def error(self, message: str):
        print(f"🛑❌ ERROR: {message}")

    def highlight(self, message: str):
        print(f"🌟💡 HIGHLIGHT: {message}")

    def divider(self):
        print("\n" + "═" * 80 + "\n")

    def summary(self, passed: int, failed: int, skipped: int):
        total_time = time.time() - self.start_time
        self.divider()
        print("📊✨ FINAL TEST EXECUTION SUMMARY ✨📊")

        table = PrettyTable()
        table.field_names = ["🏁 RESULT", "✅ PASSED", "❌ FAILED", "⏭️ SKIPPED", "⏱️ TOTAL TIME (s)"]
        table.add_row(["📋 SUMMARY", passed, failed, skipped, f"{total_time:.2f}"])
        print(table.get_string())

        if failed > 0:
            print("\n🚨 There are FAILED tests. Review immediately.")
        elif skipped > 0:
            print("\n⚠️ Some tests were SKIPPED. Double-check coverage.")
        else:
            print("\n🎉 All tests passed successfully!")
        self.divider()
