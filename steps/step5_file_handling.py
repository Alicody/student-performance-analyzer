# ============================================================
# STEP 5 — File Handling and Error Handling
# ============================================================
# Instead of hardcoding students in the script, we now READ
# them from a real CSV file on disk.
#
# New concepts:
#   - open() and the csv module
#   - try / except / else / finally
#   - FileNotFoundError, ValueError
#   - Input validation with a while loop
# ============================================================

import csv      # built-in module — no installation needed
import os       # helps us build file paths that work on any OS

# Build a path to our CSV that works no matter where you run
# the script from.
# __file__       → the full path of THIS script
# os.path.dirname → the folder containing it  (steps/)
# os.path.join   → joins path parts safely    (steps/../data/...)
# os.path.abspath → resolves it to a clean absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "student_performance.csv")


# ─────────────────────────────────────────────────────────────
# FUNCTION 1 — load_students
# Reads the CSV and returns a clean list of student dicts.
# Handles: missing file, bad/corrupt rows.
# ─────────────────────────────────────────────────────────────
def load_students(filepath):
    """
    Read student records from a CSV file.
    Returns a list of dicts with correct data types.
    Returns an empty list if the file cannot be read.
    """
    students = []

    # ── try/except: attempt risky code; catch specific errors ──
    # If ANY line inside 'try' raises an error, Python jumps
    # straight to the matching 'except' block.
    try:
        file = open(filepath, "r", newline="", encoding="utf-8")

    except FileNotFoundError:
        # This runs ONLY if the file doesn't exist at that path
        print(f"  ❌ Error: File not found → {filepath}")
        print("     Make sure 'student_performance.csv' is in the data/ folder.")
        return students   # return empty list — don't crash

    except PermissionError:
        # The file exists but we don't have read access
        print(f"  ❌ Error: Permission denied → {filepath}")
        return students

    # ── else: runs only if try succeeded (no exception raised) ──
    else:
        # csv.DictReader reads each row as a dict
        # Keys come from the first (header) row automatically
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):
            # enumerate gives us a counter alongside each item
            # start=2 because row 1 is the header
            try:
                student = {
                    "id":         int(row["student_id"]),
                    "name":       row["name"].strip(),
                    "city":       row["city"].strip(),
                    "course":     row["course"].strip(),
                    "score":      int(row["score"]),        # could raise ValueError
                    "attendance": float(row["attendance"]), # could raise ValueError
                }
                students.append(student)

            except ValueError as e:
                # ValueError happens when int("abc") or float("") etc.
                print(f"  ⚠️  Skipping row {row_number} — invalid data: {e}")
                continue   # skip this row and keep going

            except KeyError as e:
                # KeyError happens when a column name doesn't exist in the CSV
                print(f"  ⚠️  Skipping row {row_number} — missing column: {e}")
                continue

    # ── finally: ALWAYS runs, whether or not an error occurred ──
    # Perfect for cleanup tasks like closing files
    finally:
        # Only close the file if it was successfully opened
        try:
            file.close()
        except UnboundLocalError:
            pass  # file was never opened (e.g. FileNotFoundError hit first)

    return students


# ─────────────────────────────────────────────────────────────
# FUNCTION 2 — get_score_threshold
# Validates user input — keeps asking until a valid number
# between 0 and 100 is entered.
# ─────────────────────────────────────────────────────────────
def get_score_threshold():
    """
    Prompt the user for a score threshold (0–100).
    Keeps looping until valid input is received.
    Returns an integer.
    """
    while True:
        raw = input("  Enter minimum score to filter (0-100): ").strip()

        try:
            value = int(raw)           # will raise ValueError if not a number
        except ValueError:
            print("  ❌ That's not a valid number. Please enter a whole number.")
            continue  # go back to the top of the while loop

        if 0 <= value <= 100:
            return value              # valid! exit the loop and return
        else:
            print("  ❌ Score must be between 0 and 100. Try again.")


# ─────────────────────────────────────────────────────────────
# FUNCTION 3 — display_students
# A simple formatted print — extracted into its own function
# so we can reuse it wherever we need a student list printed.
# ─────────────────────────────────────────────────────────────
def display_students(student_list, title="Students"):
    """Print a formatted table of students."""
    if len(student_list) == 0:
        print("  (no students to display)")
        return

    print(f"\n  {'─' * 50}")
    print(f"  {title}")
    print(f"  {'─' * 50}")
    for s in student_list:
        print(f"  [{s['id']}] {s['name']:<15} | Score: {s['score']:>3} "
              f"| Attendance: {s['attendance']:>5.1f}% | {s['course']}")
    print(f"  {'─' * 50}")
    print(f"  Total: {len(student_list)} record(s)\n")


# ─────────────────────────────────────────────────────────────
# DEMO — test the missing-file error handling
# ─────────────────────────────────────────────────────────────
def demo_missing_file():
    """Show how the program handles a non-existent file."""
    print("\n  [TEST] Loading from a path that doesn't exist...")
    bad_data = load_students("/fake/path/no_file.csv")
    print(f"  Result: {len(bad_data)} records loaded (expected 0)\n")


# ─────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 55)
    print("  STEP 5 — File Handling & Error Handling")
    print("=" * 55)

    # 1. Load from the real CSV
    print("\n  Loading student_performance.csv ...")
    students = load_students(CSV_PATH)
    print(f"  ✅ Successfully loaded {len(students)} student records.")

    # 2. Display all loaded students
    display_students(students, title="ALL STUDENTS (loaded from CSV)")

    # 3. Demo what happens with a missing file
    demo_missing_file()

    # 4. Filter students above a user-entered threshold
    print("  Filter students by score threshold:")
    threshold = get_score_threshold()

    above = [s for s in students if s["score"] >= threshold]
    display_students(above, title=f"Students with score ≥ {threshold}")
