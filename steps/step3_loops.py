# ============================================================
# STEP 3 — Loops and Collections
# ============================================================

# A list of student dictionaries — the core data structure we use
# A list  → ordered collection, defined with [ ]
# A dict  → key-value pairs, defined with { }
# Here we have a LIST of DICTS — very common in real Python programs

students = [
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

# ── TASK 1: for loop — display all students ──────────────────────────────────
# 'for s in students' means: go through each item in the list one by one
# Each item is a dict, so s["name"] gives the value for key "name"
print("=" * 55)
print("  ALL STUDENTS")
print("=" * 55)
for s in students:
    print(f"  [{s['id']}] {s['name']:<15} | {s['course']:<12} | Score: {s['score']} | City: {s['city']}")
# Note: {s['name']:<15} left-aligns the name in a 15-character wide column
#       — makes the output look neat and tabular

# ── TASK 2: total and average score ─────────────────────────────────────────
# We start total at 0 then ADD each student's score to it — called accumulation
total = 0
for s in students:
    total = total + s["score"]   # same as: total += s["score"]

average = total / len(students)  # len() gives the number of items in a list
print(f"\n  Total Score   : {total}")
print(f"  No. Students  : {len(students)}")
print(f"  Average Score : {average:.1f}")   # :.1f → show 1 decimal place

# ── TASK 3: find the highest-scoring student ────────────────────────────────
# Strategy: assume the first student is the top, then check everyone else.
# If someone beats the current top, they become the new top.
top_student = students[0]          # start with index 0 (first item)
for s in students:
    if s["score"] > top_student["score"]:
        top_student = s            # update if we found a higher score

print(f"\n  Top Student   : {top_student['name']} — Score: {top_student['score']}")

# ── TASK 4: count passed and failed ─────────────────────────────────────────
# Passing condition: score >= 50 AND attendance >= 75
passed_count = 0
failed_count = 0
for s in students:
    if s["score"] >= 50 and s["attendance"] >= 75:
        passed_count += 1   # shorthand for: passed_count = passed_count + 1
    else:
        failed_count += 1

print(f"\n  Passed : {passed_count} students")
print(f"  Failed : {failed_count} students")

# ── TASK 5: filter students by city ─────────────────────────────────────────
# We build a NEW list containing only students from Karachi
# This pattern — loop + condition + append — is called filtering
target_city = "Karachi"
karachi_students = []              # start with an empty list
for s in students:
    if s["city"] == target_city:
        karachi_students.append(s) # .append() adds an item to the end of a list

print(f"\n  Students from {target_city}:")
for s in karachi_students:
    print(f"    → {s['name']} ({s['course']})")

# ── TASK 6: while loop — interactive menu ───────────────────────────────────
# A 'while' loop keeps running as long as the condition is True.
# We use it here to keep showing the menu until the user types 'quit'.
# 'break' immediately exits the loop, no matter what.
print("\n" + "=" * 55)
print("  MINI MENU  (type 'list', 'top', 'count', or 'quit')")
print("=" * 55)

while True:                        # True means: loop forever...
    choice = input("\n  Your choice: ").strip().lower()
    # .strip() removes accidental spaces, .lower() makes input case-insensitive

    if choice == "list":
        for s in students:
            print(f"    {s['name']} — {s['score']}")
    elif choice == "top":
        print(f"    Top student: {top_student['name']} ({top_student['score']})")
    elif choice == "count":
        print(f"    Passed: {passed_count}  |  Failed: {failed_count}")
    elif choice == "quit":
        print("    Exiting menu. Goodbye!")
        break                      # ...until 'break' is hit
    else:
        print("    Unknown command. Try: list, top, count, or quit")
