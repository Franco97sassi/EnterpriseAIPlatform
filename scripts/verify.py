import subprocess
import sys


def run_tests() -> bool:
    print("Running automated tests...")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"],
        check=False,
    )

    return result.returncode == 0


def main() -> None:
    print("=== Enterprise AI Platform Verification ===")

    tests_passed = run_tests()

    if not tests_passed:
        print("\nVerification FAILED: tests did not pass.")
        sys.exit(1)

    print("\nVerification PASSED.")
    sys.exit(0)


if __name__ == "__main__":
    main()