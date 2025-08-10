from learning_python02 import SystemSGM
from typing import Optional, Dict


def choose_major(sgm: SystemSGM) -> str:
    majors = sgm.get_majors()
    if majors:
        print("Choose major:")
        for i, m in enumerate(majors, start=1):
            print(f"{i}. {m}")
        print(f"{len(majors)+1}. Add new major")
        while True:
            choice = input(f"Enter number (1-{len(majors)+1}): ").strip()
            if not choice.isdigit():
                print("Please enter a number.")
                continue
            idx = int(choice)
            if 1 <= idx <= len(majors):
                return majors[idx - 1]
            if idx == len(majors) + 1:
                return input("Enter new major name: ").strip()
            print("Invalid choice, try again.")
    return input("No majors yet. Enter the major name: ").strip()


def choose_student(sgm: SystemSGM) -> Optional[Dict]:
    students = sgm.list_students()
    if not students:
        print("No students available.")
        return None
    print("Choose a student:")
    for i, s in enumerate(students, start=1):
        grade = s.get("grade") if s.get("grade") is not None else "-"
        print(f"{i}. {s['name']} - {grade} ({s['major']})")
    choice = input(f"Enter number (1-{len(students)}): ").strip()
    if not choice.isdigit():
        print("Invalid input.")
        return None
    idx = int(choice)
    if 1 <= idx <= len(students):
        return students[idx - 1]
    print("Invalid choice.")
    return None


def show_menu():
    print("\n__ SGM Menu __")
    print("1. Add Student")
    print("2. Add Grade")
    print("3. Remove Grade")
    print("4. Results")
    print("5. Show Students")
    print("6. Filter by Major")
    print("7. Stats by Major")
    print("8. Exit")


def main():
    sgm = SystemSGM()
    while True:
        show_menu()
        choice = input("Enter choice: ").strip()
        if choice == "1":
            name = input("Enter student's name: ").strip()
            major = choose_major(sgm)
            sgm.add_student(name, major)
        elif choice == "2":
            student = choose_student(sgm)
            if student:
                grade = input(
                    f"Enter grade for {student['name']} (0-100): ").strip()
                sgm.add_grade(student['name'], grade)
        elif choice == "3":
            student = choose_student(sgm)
            if student:
                confirm = input(
                    f"Remove grade for {student['name']}? (y/n): ").strip().lower()
                if confirm in ("y", "yes"):
                    sgm.remove_grade(student['name'])
        elif choice == "4":
            sgm.results()
        elif choice == "5":
            sort = input("Sort by (1) name or (2) grade? [1/2]: ").strip()
            sort_by = "grade" if sort == "2" else "name"
            for s in sgm.list_students(sort_by=sort_by):
                grade = s.get("grade") if s.get("grade") is not None else "-"
                print(f"{s['name']} - {grade} ({s['major']})")
        elif choice == "6":
            major = choose_major(sgm)
            found = False
            for s in sgm.list_students():
                if s.get("major") == major:
                    grade = s.get("grade") if s.get(
                        "grade") is not None else "-"
                    print(f"{s['name']} - {grade} ({s['major']})")
                    found = True
            if not found:
                print(f"No students found in major: {major}")
        elif choice == "7":
            stats = sgm.stats_by_major()
            for major, data in stats.items():
                avg = f"{data['avg']:.2f}" if data['avg'] is not None else "-"
                print(
                    f"{major}: Count={data['count']}, Grades Assigned={data['grades_assigned']}, Avg={avg}")
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
