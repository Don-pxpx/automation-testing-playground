import time
from prettytable import PrettyTable

class InlineLogger:
    def __init__(self):
        self.step_counter = 1
        self.start_time = time.time()

    def step(self, description):
        print(f"\n🔵🔷🔹 ➡️ STEP {self.step_counter}: {description.upper()} 🔹🔷🔵")
        self.step_counter += 1

    def note(self, message):
        print(f"🗒️ ✍️ NOTE: {message}")

    def success(self, message):
        print(f"✅✨ SUCCESS: {message}")

    def warning(self, message):
        print(f"⚠️🚧 WARNING: {message}")

    def error(self, message):
        print(f"🛑❌ ERROR: {message}")

    def highlight(self, message):
        print(f"🌟💡 HIGHLIGHT: {message}")

    def divider(self):
        print("\n" + "═" * 80 + "\n")

    def summary(self, passed, failed, skipped):
        total_time = time.time() - self.start_time
        self.divider()
        print("📊✨ FINAL TEST EXECUTION SUMMARY ✨📊")

        table = PrettyTable()
        table.field_names = ["🏁 RESULT", "✅ PASSED", "❌ FAILED", "⏭️ SKIPPED", "⏱️ TOTAL TIME (s)"]
        table.add_row(["📋 SUMMARY", passed, failed, skipped, f"{total_time:.2f}"])
        print(table.get_string())

        if failed > 0:
            print("\n🚨🚨🚨 ATTENTION: There are FAILED tests! Review Immediately! 🚨🚨🚨")
        elif skipped > 0:
            print("\n⚠️⚠️⚠️ Some tests were SKIPPED. Please double-check coverage. ⚠️⚠️⚠️")
        else:
            print("\n🎉🎉🎉 ALL TESTS PASSED SUCCESSFULLY! WELL DONE! 🎉🎉🎉")
        self.divider()
