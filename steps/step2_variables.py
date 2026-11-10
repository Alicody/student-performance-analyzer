# ============================================================
# STEP 2 — Variables, Data Types and Conditions
# ============================================================

# ── TASK 1: Store student details using correct data types ──
student_id = 101          # int   → whole numbers, no decimal
name       = "Ali Hassan" # str   → text, always in quotes
city       = "Karachi"    # str
course     = "Python"     # str
score      = 88           # int   → score out of 100
attendance = 92.0         # float → percentage, can have decimals

# ── TASK 2: Display student info using an f-string ──
# f-strings let you embed variables directly inside a string
# Syntax: f"some text {variable} more text"
print("=" * 40)
print("       STUDENT REPORT CARD")
print("=" * 40)
print(f"  ID         : {student_id}")
print(f"  Name       : {name}")
print(f"  City       : {city}")
print(f"  Course     : {course}")
print(f"  Score      : {score}")
print(f"  Attendance : {attendance}%")

# ── TASK 3: Assign a grade using if / elif / else ──
# Python checks conditions top to bottom and stops at the first True one.
# Boundaries matter: 90 and above is A, 75-89 is B, etc.
if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 60:
    grade = "C"
elif score >= 50:
    grade = "D"
else:
    grade = "F"

print(f"  Grade      : {grade}")

# ── TASK 4: Did the student pass? ──
# Passing needs BOTH conditions to be True → use 'and'
# If only one condition needs to be True, you would use 'or'
passed = score >= 50 and attendance >= 75

print(f"  Passed     : {'Yes ✅' if passed else 'No ❌'}")
print("=" * 40)

# ── BONUS: Show data types ──
# type() tells you what kind of data a variable holds
print("\n--- Data Types ---")
print(f"  student_id → {type(student_id)}")
print(f"  name       → {type(name)}")
print(f"  score      → {type(score)}")
print(f"  attendance → {type(attendance)}")
print(f"  passed     → {type(passed)}")
