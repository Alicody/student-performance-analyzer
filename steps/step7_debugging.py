# ============================================================
# STEP 7 — Debugging and Code Improvement
# ============================================================
# This file originally had 3 intentional bugs + 1 edge case.
# Below you will see:
#   1. Each bug clearly identified with a comment
#   2. The fix applied
#   3. Additional improvements: edge cases, naming, cleanup
# ============================================================

import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "student_performance.csv")


# ─────────────────────────────────────────────────────────────
# FUNCTION 1 — load_students (fixed)
# ─────────────────────────────────────────────────────────────
def load_students(filepath):
    """Load student records from a CSV file. Returns a list of dicts."""
    students = []

    try:
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    students.append({
                        "id":         int(row["student_id"]),
                        "name":       row["name"].strip(),
                        "city":       row["city"].strip(),
                        "course":     row["course"].strip(),

                        # ✅ BUG 1 FIXED ────────────────────────────────
                        # ORIGINAL (broken):  int(row["scor"])
                        #   → KeyError: 'scor' (typo — column is "score")
                        # FIX: use the correct column name "score"
                        "score":      int(row["score"]),

                        "attendance": float(row["attendance"]),
                    })
                except (ValueError, KeyError) as e:
                    print(f"  ⚠️  Skipping bad row: {e}")
                    continue

    except FileNotFoundError:
        print(f"  ❌ File not found: {filepath}")

    return students


# ─────────────────────────────────────────────────────────────
# FUNCTION 2 — calculate_average (fixed)
# ─────────────────────────────────────────────────────────────
def calculate_average(students):
    """Return the average score. Returns 0 for an empty list."""

    # Edge case: empty list would cause ZeroDivisionError
    if len(students) == 0:
        return 0

    total = 0
    for s in students:

        # ✅ BUG 2 FIXED ────────────────────────────────────────
        # ORIGINAL (broken):  total == total + s["score"]
        #   → '==' is COMPARISON (True/False), not assignment!
        #   → total never actually changed — always stayed 0
        # FIX: use '=' (assignment)
        total = total + s["score"]   # or: total += s["score"]

    return total / len(students)


# ─────────────────────────────────────────────────────────────
# FUNCTION 3 — find_top_student (fixed)
# ─────────────────────────────────────────────────────────────
def find_top_student(students):
    """Return the student dict with the highest score."""

    # Edge case: can't find a top student in an empty list
    if len(students) == 0:
        return None

    top = students[0]
    for s in students:

        # ✅ BUG 3 FIXED ────────────────────────────────────────
        # ORIGINAL (broken):  if s["score"] < top["score"]:
        #   → '<' finds the LOWEST scorer, not the highest!
        # FIX: use '>' to find the highest scorer
        if s["score"] > top["score"]:
            top = s

    return top


# ─────────────────────────────────────────────────────────────
# FUNCTION 4 — safe_average (edge case handled)
# ─────────────────────────────────────────────────────────────
def safe_average(students):
    """
    Calculate average safely.
    Returns 0 and prints a message if the list is empty.
    """

    # ✅ EDGE CASE: what if no students are loaded?
    # Without this check: ZeroDivisionError → program crashes
    if not students:   # 'not students' is True when list is empty
        print("  ⚠️  No students found — cannot calculate average.")
        return 0

    return calculate_average(students)


# ─────────────────────────────────────────────────────────────
# FUNCTION 5 — display_summary (improved)
# ─────────────────────────────────────────────────────────────
def display_summary(students):
    """Print a clean performance summary."""

    print("\n" + "=" * 45)
    print("  STUDENT PERFORMANCE SUMMARY")
    print("=" * 45)

    # Edge case: handle empty dataset gracefully
    if not students:
        print("  No student data to display.")
        print("=" * 45)
        return

    print(f"  Total Students : {len(students)}")
    print(f"  Average Score  : {calculate_average(students):.1f}")

    top = find_top_student(students)
    if top:
        print(f"  Top Student    : {top['name']} ({top['score']})")

    passed = [s for s in students if s["score"] >= 50 and s["attendance"] >= 75]
    failed = [s for s in students if not (s["score"] >= 50 and s["attendance"] >= 75)]
    print(f"  Passed         : {len(passed)}")
    print(f"  Failed         : {len(failed)}")
    print("=" * 45)


# ─────────────────────────────────────────────────────────────
# MAIN — demonstrate all fixes and edge cases
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 55)
    print("  STEP 7 — Debugging and Code Improvement")
    print("=" * 55)

    # ── Show the 3 bugs clearly ───────────────────────────────
    print("""
  ┌─ BUGS FOUND AND FIXED ───────────────────────────────┐
  │                                                       │
  │  BUG 1 — KeyError typo                               │
  │    int(row["scor"])  →  int(row["score"])            │
  │                                                       │
  │  BUG 2 — == used instead of = (comparison vs assign) │
  │    total == total + score  →  total = total + score   │
  │                                                       │
  │  BUG 3 — Wrong comparison operator                   │
  │    if score < top["score"]  →  if score > top["score"]│
  │                                                       │
  └───────────────────────────────────────────────────────┘
""")

    # ── Load real data ────────────────────────────────────────
    print("  Loading CSV...")
    students = load_students(CSV_PATH)
    print(f"  ✅ Loaded {len(students)} records\n")

    # ── Verify BUG 2 fix: average must NOT be 0 ──────────────
    avg = calculate_average(students)
    print(f"  Average Score (Bug 2 fix check)  : {avg:.1f}  ← should be ~71.2, not 0")

    # ── Verify BUG 3 fix: top must be Fatima (95), not Nadia (38) ──
    top = find_top_student(students)
    print(f"  Top Student  (Bug 3 fix check)   : {top['name']} ({top['score']})  ← should be Fatima Raza (95)")

    # ── Edge case: empty list ─────────────────────────────────
    print("\n  ── Edge Case: Empty List ──")
    print(f"  safe_average([])   →  {safe_average([])}")
    print(f"  find_top_student([]) →  {find_top_student([])}")
    display_summary([])

    # ── Edge case: missing file ───────────────────────────────
    print("\n  ── Edge Case: Missing File ──")
    bad = load_students("/nonexistent/path.csv")
    print(f"  load_students(bad path) → {len(bad)} records")

    # ── Full summary on real data ─────────────────────────────
    display_summary(students)

    # ── Error type reference ──────────────────────────────────
    print("""
  ┌─ 3 TYPES OF ERRORS IN PYTHON ────────────────────────┐
  │                                                       │
  │  1. Syntax Error    — code won't even run             │
  │     e.g. missing colon:  if x > 5                    │
  │                                                       │
  │  2. Runtime Error   — crashes while running           │
  │     e.g. int("abc"),  1/0,  file not found           │
  │                                                       │
  │  3. Logic Error     — runs fine, but wrong result     │
  │     e.g. == instead of =,  < instead of >            │
  │     Hardest to spot — no error message!              │
  │                                                       │
  └───────────────────────────────────────────────────────┘
""")
