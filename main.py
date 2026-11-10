# ============================================================
# STEP 8 — Final Application
# main.py — Student Performance Analyzer
# ============================================================
# This file brings together EVERY concept from Steps 2–7:
#   ✅ Variables & data types      (Step 2)
#   ✅ Loops & collections         (Step 3)
#   ✅ Functions                   (Step 4)
#   ✅ File handling & errors      (Step 5)
#   ✅ OOP — Student class         (Step 6)
#   ✅ Debugging & edge cases      (Step 7)
#
# Run it with: python3 main.py
# ============================================================

import csv
import os

# ─────────────────────────────────────────────────────────────
# PATH SETUP
# ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "student_performance.csv")


# ═════════════════════════════════════════════════════════════
#  STUDENT CLASS  (from Step 6)
# ═════════════════════════════════════════════════════════════
class Student:
    """Blueprint for a student — bundles data + behaviour together."""

    def __init__(self, student_id, name, city, course, score, attendance):
        self.student_id = student_id
        self.name       = name
        self.city       = city
        self.course     = course
        self.score      = score
        self.attendance = attendance

    def get_grade(self):
        """Return a letter grade based on score."""
        if self.score >= 90:   return "A"
        elif self.score >= 75: return "B"
        elif self.score >= 60: return "C"
        elif self.score >= 50: return "D"
        else:                  return "F"

    def has_passed(self):
        """Return True if score >= 50 AND attendance >= 75."""
        return self.score >= 50 and self.attendance >= 75

    def __str__(self):
        status = "Pass ✅" if self.has_passed() else "Fail ❌"
        return (
            f"  [{self.student_id}] {self.name:<15} | "
            f"Course: {self.course:<12} | "
            f"Score: {self.score:>3} | "
            f"Attendance: {self.attendance:>5.1f}% | "
            f"Grade: {self.get_grade()} | {status}"
        )


# ═════════════════════════════════════════════════════════════
#  DATA LAYER  (from Step 5)
# ═════════════════════════════════════════════════════════════
def load_students(filepath):
    """
    Read the CSV and return a list of Student objects.
    Handles missing file and bad rows gracefully.
    """
    students = []
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    students.append(Student(
                        student_id = int(row["student_id"]),
                        name       = row["name"].strip(),
                        city       = row["city"].strip(),
                        course     = row["course"].strip(),
                        score      = int(row["score"]),
                        attendance = float(row["attendance"]),
                    ))
                except (ValueError, KeyError):
                    continue   # skip corrupted rows silently

    except FileNotFoundError:
        print(f"\n  ❌ Could not find: {filepath}")
        print("     Make sure 'student_performance.csv' is inside the data/ folder.\n")
    except PermissionError:
        print(f"\n  ❌ Permission denied: {filepath}\n")

    return students


# ═════════════════════════════════════════════════════════════
#  BUSINESS LOGIC  (from Steps 3 & 4)
# ═════════════════════════════════════════════════════════════
def get_average(students, field="score"):
    """Return the average of a numeric field across all students."""
    if not students:
        return 0
    return sum(getattr(s, field) for s in students) / len(students)
    # getattr(obj, "score") is the same as obj.score
    # but lets us choose the field dynamically


def get_top_student(students):
    """Return the Student with the highest score."""
    if not students:
        return None
    return max(students, key=lambda s: s.score)


def filter_by_city(students, city):
    """Return students whose city matches (case-insensitive)."""
    return [s for s in students if s.city.lower() == city.lower()]


def filter_above_score(students, threshold):
    """Return students whose score is >= threshold."""
    return [s for s in students if s.score >= threshold]


def count_by_course(students):
    """Return a dict of {course_name: student_count}."""
    counts = {}
    for s in students:
        counts[s.course] = counts.get(s.course, 0) + 1
    return counts


# ═════════════════════════════════════════════════════════════
#  UI HELPERS
# ═════════════════════════════════════════════════════════════
def print_header(title):
    """Print a section header."""
    print(f"\n  {'─' * 52}")
    print(f"  {title}")
    print(f"  {'─' * 52}")


def print_student_list(students, title="Results"):
    """Print a formatted list of Student objects."""
    print_header(title)
    if not students:
        print("  (no matching students found)")
    else:
        for s in students:
            print(s)
        print(f"\n  Total: {len(students)} student(s)")


def get_valid_int(prompt, lo=0, hi=100):
    """
    Ask the user for an integer between lo and hi.
    Keeps looping until a valid value is entered.
    """
    while True:
        raw = input(f"  {prompt}").strip()
        try:
            value = int(raw)
            if lo <= value <= hi:
                return value
            print(f"  ❌ Please enter a number between {lo} and {hi}.")
        except ValueError:
            print("  ❌ That's not a valid number. Try again.")


def get_valid_string(prompt):
    """Ask the user for a non-empty string."""
    while True:
        raw = input(f"  {prompt}").strip()
        if raw:
            return raw
        print("  ❌ Input cannot be empty. Try again.")


# ═════════════════════════════════════════════════════════════
#  MENU ACTIONS  — one function per menu option
# ═════════════════════════════════════════════════════════════
def action_view_all(students):
    """Menu option 1 — display all students."""
    print_student_list(students, title=f"ALL STUDENTS  ({len(students)} total)")


def action_averages(students):
    """Menu option 2 — average score and attendance."""
    print_header("AVERAGES")
    avg_score      = get_average(students, "score")
    avg_attendance = get_average(students, "attendance")
    passed = [s for s in students if s.has_passed()]

    print(f"  Average Score      : {avg_score:.1f} / 100")
    print(f"  Average Attendance : {avg_attendance:.1f} %")
    print(f"  Passed             : {len(passed)} / {len(students)} students")
    print(f"  Failed             : {len(students) - len(passed)} / {len(students)} students")


def action_top_student(students):
    """Menu option 3 — highest-scoring student."""
    print_header("TOP STUDENT")
    top = get_top_student(students)
    if top:
        print(top)
    else:
        print("  No data available.")


def action_filter_city(students):
    """Menu option 4 — filter by city."""
    city = get_valid_string("Enter city name: ")
    results = filter_by_city(students, city)
    print_student_list(results, title=f"STUDENTS FROM  {city.upper()}")


def action_filter_score(students):
    """Menu option 5 — search above a score threshold."""
    threshold = get_valid_int("Enter minimum score (0–100): ", 0, 100)
    results   = filter_above_score(students, threshold)
    print_student_list(results, title=f"STUDENTS WITH SCORE ≥ {threshold}")


def action_course_counts(students):
    """Menu option 6 — student count per course."""
    print_header("STUDENTS BY COURSE")
    counts = count_by_course(students)
    if not counts:
        print("  No data available.")
        return
    for course, count in sorted(counts.items()):
        bar = "█" * count          # tiny ASCII bar chart
        print(f"  {course:<15} : {count:>2} student(s)  {bar}")


# ═════════════════════════════════════════════════════════════
#  MAIN — the entry point
# ═════════════════════════════════════════════════════════════
def main():
    # ── Banner ───────────────────────────────────────────────
    print("\n" + "=" * 56)
    print("       🎓  STUDENT PERFORMANCE ANALYZER  🎓")
    print("=" * 56)

    # ── Load data once at startup ─────────────────────────────
    print(f"\n  Loading data from: {os.path.basename(CSV_PATH)} ...")
    students = load_students(CSV_PATH)

    if not students:
        print("  ❌ No student data loaded. Exiting.")
        return                    # exit main() — nothing to analyze

    print(f"  ✅ {len(students)} student records loaded successfully!")

    # ── Menu map: choice → function ───────────────────────────
    # A dictionary of functions — calling a function stored in a dict
    # is a clean pattern to avoid a long chain of if/elif/elif...
    menu_options = {
        "1": ("View all students",                    lambda: action_view_all(students)),
        "2": ("View average score and attendance",    lambda: action_averages(students)),
        "3": ("Find the highest-scoring student",     lambda: action_top_student(students)),
        "4": ("Filter students by city",              lambda: action_filter_city(students)),
        "5": ("Search students above a score",        lambda: action_filter_score(students)),
        "6": ("View student counts by course",        lambda: action_course_counts(students)),
        "7": ("Exit",                                 None),
    }

    # ── Interactive menu loop ─────────────────────────────────
    while True:
        print("\n" + "─" * 56)
        print("  MAIN MENU")
        print("─" * 56)
        for key, (label, _) in menu_options.items():
            print(f"    {key}. {label}")
        print("─" * 56)
        

        choice = input("  Enter your choice (1–7): ").strip()

        if choice not in menu_options:
            print("  ❌ Invalid choice. Please enter a number from 1 to 7.")
            continue

        label, action = menu_options[choice]

        if choice == "7":
            print("\n  Goodbye! Keep learning and keep building. 🚀")
            print("=" * 56 + "\n")
            break                 # exit the while loop → program ends

        # Call whichever function matches the user's choice
        action()


# ── Guard: only run main() when this file is executed directly ──
if __name__ == "__main__":
    main()
