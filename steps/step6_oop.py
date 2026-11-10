# ============================================================
# STEP 6 — Object-Oriented Programming (OOP)
# ============================================================
# So far we stored student data in plain dictionaries.
# OOP lets us bundle DATA (attributes) + BEHAVIOUR (methods)
# together into a single blueprint called a CLASS.
#
# Real-world analogy:
#   Class  → the blueprint for a house
#   Object → an actual house built from that blueprint
#   Each house has the same structure but different values
#   (different address, colour, size).
# ============================================================

import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "student_performance.csv")


# ─────────────────────────────────────────────────────────────
# THE CLASS
# ─────────────────────────────────────────────────────────────
class Student:
    """
    Represents a single student with their performance data.

    Attributes:
        student_id (int)  : unique identifier
        name       (str)  : full name
        city       (str)  : city of residence
        course     (str)  : enrolled course
        score      (int)  : exam score out of 100
        attendance (float): attendance percentage
    """

    # ── __init__ ──────────────────────────────────────────────
    # Called automatically when you do: Student(101, "Ali", ...)
    # 'self' is a reference to the specific object being created.
    # Every method MUST have 'self' as its first parameter —
    # Python passes it automatically; you don't type it when calling.
    def __init__(self, student_id, name, city, course, score, attendance):
        self.student_id = student_id   # self.X saves X onto THIS object
        self.name       = name
        self.city       = city
        self.course     = course
        self.score      = score
        self.attendance = attendance

    # ── get_grade ─────────────────────────────────────────────
    # A METHOD is just a function that lives inside a class.
    # It has access to all the object's data through 'self'.
    def get_grade(self):
        """Return a letter grade based on this student's score."""
        if self.score >= 90:
            return "A"
        elif self.score >= 75:
            return "B"
        elif self.score >= 60:
            return "C"
        elif self.score >= 50:
            return "D"
        else:
            return "F"

    # ── has_passed ────────────────────────────────────────────
    def has_passed(self):
        """Return True if score >= 50 AND attendance >= 75."""
        return self.score >= 50 and self.attendance >= 75

    # ── get_status ────────────────────────────────────────────
    def get_status(self):
        """Return a human-readable pass/fail string."""
        return "Pass ✅" if self.has_passed() else "Fail ❌"

    # ── __str__ ───────────────────────────────────────────────
    # Python calls __str__ automatically when you use print(object)
    # or str(object). Without it, print would show something ugly
    # like: <__main__.Student object at 0x10f3a2c50>
    def __str__(self):
        return (
            f"[{self.student_id}] {self.name:<15} | "
            f"Course: {self.course:<12} | "
            f"Score: {self.score:>3} | "
            f"Attendance: {self.attendance:>5.1f}% | "
            f"Grade: {self.get_grade()} | "
            f"{self.get_status()}"
        )


# ─────────────────────────────────────────────────────────────
# HELPER — load Student OBJECTS from CSV
# In Step 5 we loaded plain dicts. Now we create Student objects.
# ─────────────────────────────────────────────────────────────
def load_student_objects(filepath):
    """Read CSV and return a list of Student objects."""
    students = []
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            # 'with open(...)' is the preferred way to open files.
            # It automatically closes the file when the block ends,
            # even if an error occurs — no need for a finally block.
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    s = Student(
                        student_id = int(row["student_id"]),
                        name       = row["name"].strip(),
                        city       = row["city"].strip(),
                        course     = row["course"].strip(),
                        score      = int(row["score"]),
                        attendance = float(row["attendance"]),
                    )
                    students.append(s)
                except (ValueError, KeyError):
                    continue   # skip bad rows silently

    except FileNotFoundError:
        print(f"  ❌ File not found: {filepath}")

    return students


# ─────────────────────────────────────────────────────────────
# HELPER FUNCTIONS — now work with Student OBJECTS not dicts
# ─────────────────────────────────────────────────────────────
def get_average_score(students):
    """Return average score across all Student objects."""
    if not students:
        return 0
    return sum(s.score for s in students) / len(students)


def get_top_student(students):
    """Return the Student object with the highest score."""
    if not students:
        return None
    return max(students, key=lambda s: s.score)


def filter_by_city(students, city):
    """Return Student objects whose city matches (case-insensitive)."""
    return [s for s in students if s.city.lower() == city.lower()]


def count_by_course(students):
    """Return dict of {course: count}."""
    counts = {}
    for s in students:
        counts[s.course] = counts.get(s.course, 0) + 1
        # dict.get(key, default) → returns default if key not found
        # cleaner than the if/else approach we used in Step 4
    return counts


def get_passed_failed(students):
    """Return (passed_list, failed_list) as a tuple."""
    passed = [s for s in students if s.has_passed()]
    failed = [s for s in students if not s.has_passed()]
    return passed, failed   # returning TWO values as a tuple


# ─────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 70)
    print("  STEP 6 — Object-Oriented Programming")
    print("=" * 70)

    # 1. Create a few objects manually to see how it works
    print("\n── Manual Object Creation ──")
    s1 = Student(101, "Ali Hassan",  "Karachi",   "Python",       88, 92.0)
    s2 = Student(104, "Ayesha Noor", "Karachi",   "AI",           91, 97.0)
    s3 = Student(106, "Zara Malik",  "Islamabad", "Data Science", 49, 60.0)

    for obj in [s1, s2, s3]:
        print(obj)   # triggers __str__ automatically

    # 2. Accessing individual attributes and methods
    print(f"\n  s1.name      → {s1.name}")
    print(f"  s1.score     → {s1.score}")
    print(f"  s1.get_grade() → {s1.get_grade()}")
    print(f"  s3.has_passed() → {s3.has_passed()}  (score={s3.score}, attendance={s3.attendance})")

    # 3. Load ALL students from CSV as objects
    print("\n── Loaded from CSV ──")
    students = load_student_objects(CSV_PATH)
    print(f"  Loaded {len(students)} Student objects\n")
    for s in students:
        print(f"  {s}")

    # 4. Use helper functions
    avg = get_average_score(students)
    top = get_top_student(students)
    passed, failed = get_passed_failed(students)   # unpacking the tuple

    print(f"\n  Average Score : {avg:.1f}")
    print(f"  Top Student   : {top.name} (Score: {top.score}, Grade: {top.get_grade()})")
    print(f"  Passed        : {len(passed)} students")
    print(f"  Failed        : {len(failed)} students")

    # 5. Filter by city
    print("\n── Karachi Students ──")
    for s in filter_by_city(students, "Karachi"):
        print(f"  {s.name} — {s.course}")

    # 6. Course breakdown
    print("\n── Students by Course ──")
    for course, count in count_by_course(students).items():
        print(f"  {course:<15} : {count} student(s)")
