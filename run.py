import os

def run_tests():
    print("\nChoose which test suite you want to run:")
    print("[s] Smoke tests")
    print("[n] Negative tests")
    print("[u] UI tests")
    print("[v] Validation tests")
    print("[a] All tests")
    print("[q] Quit")

    choice = input("Enter your choice: ").strip().lower()

    if choice == 's':
        os.system("pytest -m smoke")
    elif choice == 'n':
        os.system("pytest -m negative")
    elif choice == 'u':
        os.system("pytest -m ui")
    elif choice == 'v':
        os.system("pytest -m validation")
    elif choice == 'a':
        os.system("pytest -v")
    elif choice == 'q':
        print("Exiting...")
    else:
        print("❌ Invalid choice. Please select again.")
        run_tests()

if __name__ == "__main__":
    run_tests()
