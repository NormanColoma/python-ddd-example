import sys
import subprocess

def main():
    format_result = subprocess.call(["ruff", "format", "."])
    if format_result != 0:
        print("❌ Error during formatting.")
        sys.exit(format_result)

    lint_result = subprocess.call(["ruff", "check", ".", "--fix"])
    if lint_result != 0:
        print("❌ Linting found issues that couldn't be fixed automatically.")
        sys.exit(lint_result)

    print("✅ Lint completed successfully.")
