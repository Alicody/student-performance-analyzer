# ============================================================
# STEP 4 — Functions
# ============================================================
# Functions let us give a block of code a name so we can
# REUSE it without copy-pasting.
#
# Anatomy of a function:
#   def function_name(parameter1, parameter2):
#       """Docstring — explains what the function does."""
#       # body — the logic
#       return result   ← sends a value back to the caller
# ============================================================

# Same dataset — in Step 5 we'll load this from a CSV file instead
STUDENTS = [
    {"id": 101, "name": "Ali Hassan",   "city": "Karachi",   "course": "Python",       "score": 88, "attendance": 92},
    {"id": 102, "name": "Sara Khan",    "city": "Lahore",    "course": "Data Science", "score": 74, "attendance": 85},
    {"id": 103, "name": "Bilal Ahmed",  "city": "Islamabad", "course": "Python",       "score": 55, "attendance": 70},
    {"id": 104, "name": "Ayesha Noor", "city": "Karachi",   "course": "AI",           "score": 91, "attendance": 97},
    {"id": 105, "name": "Omar Sheikh",  "city": "Lahore",    "course": "Python",       "score": 63, "attendance": 78},
    {"id": 106, "name": "Zara Malik",   "city": "Islamabad", "course": "Data Science", "score": 49, "attendance": 60},
    {"id": 107, "name": "Hassan Ali",   "city": "Karachi",   "course": "AI",           "score": 77, "attendance": 88},
    {"id": 108, "name": "Fatima Raza",  "city": "Lahore",    "course": "Python",       "score": 95, "attendance": 99},
    {"id": 109, "name": "Usman Tariq",  "city": "Islamabad", "course": "Data Science", "score": 82, "attendance": 91},
    {"id": 110, "name": "Nadia Butt",   "city": "Karachi",   "course": "AI",           "score": 38, "attendance": 55},
]

# ─────────────────────────────────────────────────────────────────────────────
# FUNCTION 1 — load_students
# Returns the list of student records.
# In Step 5, this will read from a real CSV file.
# Right now it just returns our hardcoded list.
# ─────────────────────────────────────────────────────────────────────────────
def load_students():
    """Return the full list of student dictionaries."""
    return STUDENTS


# ─────────────────────────────────────────────────────────────────────────────
# FUNCTION 2 — calculate_average
# Takes the list as a parameter → does the work → returns a float.
# 'student_list' only exists INSIDE this function (local scope).
# ─────────────────────────────────────────────────────────────────────────────
def calculate_average(student_list):
    """Return the average score across all students."""
    if len(student_list) == 0:       # guard against dividing by zero
        return 0
    total = sum(s["score"] for s in student_list)  # sum() + generator expression
    return total / len(student_list)


# ─────────────────────────────────────────────────────────────────────────────
# FUNCTION 3 — find_top_student
# Returns the entire student DICTIONARY of the highest scorer,
# not just the name — so the caller can access any field they need.
# ─────────────────────────────────────────────────────────────────────────────
def find_top_student(student_list):
    """Return the student dictionary with the highest score."""
    if len(student_list) == 0:
        return None
    # max() with a 'key' argument — key tells max() WHAT to compare
    return max(student_list, key=lambda s: s["score"])
    # lambda s: s["score"]  is a tiny anonymous function:
    #   "for each student s, use s['score'] as the comparison value"


# ─────────────────────────────────────────────────────────────────────────────
# FUNCTION 4 — filter_by_city
# Takes TWO parameters: the list AND the city to filter by.
# Returns a new list — does not modify the original.
# ─────────────────────────────────────────────────────────────────────────────
def filter_by_city(student_list, city):
    """Return a list of students whose city matches the given city."""
    # List comprehension: a compact way to build a filtered list
    # Equivalent to: loop + if + append — but in one line
    return [s for s in student_list if s["city"].lower() == city.lower()]


# ─────────────────────────────────────────────────────────────────────────────
# FUNCTION 5 — count_by_course
# Returns a DICTIONARY where each key is a course name
# and the value is how many students are in it.
# ─────────────────────────────────────────────────────────────────────────────
def count_by_course(student_list):
    """Return a dict of {course_name: student_count}."""
    counts = {}
    for s in student_list:
        course = s["course"]
        if course in counts:
            counts[course] += 1    # course already seen — increment
        else:
            counts[course] = 1     # first time seeing this course — start at 1
    return counts


# ─────────────────────────────────────────────────────────────────────────────
# FUNCTION 6 — display_summary
# This function PRINTS — it does not return a value.
# It calls the other functions above (functions calling functions).
# ─────────────────────────────────────────────────────────────────────────────
def display_summary(student_list):
    """Print a summary report for the given list of students."""
    print("=" * 45)
    print("  STUDENT PERFORMANCE SUMMARY")
    print("=" * 45)
    print(f"  Total Students  : {len(student_list)}")
    print(f"  Average Score   : {calculate_average(student_list):.1f}")

    top = find_top_student(student_list)
    if top:
        print(f"  Top Student     : {top['name']} ({top['score']})")

    print("\n  Students by Course:")
    for course, count in count_by_course(student_list).items():
        # .items() gives us (key, value) pairs from a dict
        print(f"    {course:<15} → {count} student{'s' if count != 1 else ''}")

    print("\n  Students by City:")
    for city in ["Karachi", "Lahore", "Islamabad"]:
        city_students = filter_by_city(student_list, city)
        print(f"    {city:<12} → {len(city_students)} student{'s' if len(city_students) != 1 else ''}")
    print("=" * 45)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN EXECUTION — this only runs when you execute this file directly
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Load data using our function
    students = load_students()

    # Call and print individual functions
    print(f"Average Score : {calculate_average(students):.1f}")
    print(f"Top Student   : {find_top_student(students)['name']}")
    print(f"Karachi List  : {[s['name'] for s in filter_by_city(students, 'Karachi')]}")
    print(f"Course Counts : {count_by_course(students)}")
    print()

    # Full summary
    display_summary(students)
