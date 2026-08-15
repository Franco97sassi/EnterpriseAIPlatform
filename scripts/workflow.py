import subprocess
import sys


def run_command(command: list[str], description: str) -> bool:
    print(f"\n=== {description} ===")

    result = subprocess.run(
        command,
        check=False,
    )

    return result.returncode == 0


def main() -> None:
    print("=== Enterprise AI Platform Development Workflow ===")

    print("\n[1/5] PLAN")
    print("Task requirements must be defined before implementation.")

    print("\n[2/5] IMPLEMENT")
    print("Implementation must follow AGENTS.md.")

    print("\n[3/5] TEST")
    tests_passed = run_command(
        [sys.executable, "-m", "pytest", "-v"],
        "Running tests",
    )

    if not tests_passed:
        print("\nWorkflow FAILED during TEST.")
        sys.exit(1)

    print("\n[4/5] VERIFY")
    verification_passed = run_command(
        [sys.executable, "scripts/verify.py"],
        "Running verification",
    )

    if not verification_passed:
        print("\nWorkflow FAILED during VERIFY.")
        sys.exit(1)

    print("\n[5/5] REVIEW")
    print("Manual or AI-assisted code review required.")

    print("\n=== WORKFLOW PASSED ===")


if __name__ == "__main__":
    main()