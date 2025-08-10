import json
import os
from typing import List, Dict, Optional


class SystemSGM:
    """Simple Student Grade Manager.

    Student format:
        {"name": str, "major": str, "grade": Optional[int]}
    """

    def __init__(self, filename: str = "data/SGM.json"):
        self.filename = filename
        self.students: List[Dict] = []
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.students = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.students = []
        else:
            self.students = []

    def save_data(self):
        folder = os.path.dirname(self.filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.students, f, ensure_ascii=False, indent=4)

    def find_student(self, name: str) -> Optional[Dict]:
        name = (name or "").strip()
        for s in self.students:
            if s.get("name", "").lower() == name.lower():
                return s
        return None

    def add_student(self, name: str, major: str) -> bool:
        if not name:
            print("Name cannot be empty.")
            return False
        if self.find_student(name):
            print(f"Student '{name}' already exists.")
            return False
        student = {"name": name.strip(), "major": (
            major or "").strip(), "grade": None}
        self.students.append(student)
        self.save_data()
        print(f"Added student: {student['name']} ({student['major']})")
        return True

    def add_grade(self, name: str, grade) -> bool:
        student = self.find_student(name)
        if not student:
            print(f"Student '{name}' not found.")
            return False
        try:
            g = int(grade)
        except (ValueError, TypeError):
            print("Grade must be an integer between 0 and 100.")
            return False
        if g < 0 or g > 100:
            print("Grade must be between 0 and 100.")
            return False
        student["grade"] = g
        self.save_data()
        print(f"Assigned grade {g} to {student['name']}.")
        return True

    def remove_grade(self, name: str) -> bool:
        student = self.find_student(name)
        if not student:
            print(f"Student '{name}' not found.")
            return False
        student["grade"] = None
        self.save_data()
        print(f"Removed grade for {student['name']}.")
        return True

    def results(self):
        best = []
        accepted = []
        failed = []
        no_grade = []

        for s in self.students:
            g = s.get("grade")
            if g is None:
                no_grade.append(s)
                continue
            if g >= 70:
                best.append(s)
            elif 50 <= g < 70:
                accepted.append(s)
            else:
                failed.append(s)

        print("\n-- Results --")

        print("\nBest students (>= 70):")
        if best:
            for s in best:
                print(f"  {s['name']} - {s['grade']} ({s['major']})")
        else:
            print("  (none)")

        print("\nAccepted (50-69):")
        if accepted:
            for s in accepted:
                print(f"  {s['name']} - {s['grade']} ({s['major']})")
        else:
            print("  (none)")

        print("\nFailed (< 50):")
        if failed:
            for s in failed:
                print(f"  {s['name']} - {s['grade']} ({s['major']})")
        else:
            print("  (none)")

        print("\nNo grade assigned:")
        if no_grade:
            for s in no_grade:
                print(f"  {s['name']} ({s['major']})")
        else:
            print("  (none)")

    def get_majors(self) -> List[str]:
        return sorted({(s.get("major") or "Unknown") for s in self.students})

    def list_students(self, sort_by: str = "name") -> List[Dict]:
        if sort_by == "grade":
            return sorted(self.students, key=lambda s: (s.get("grade") is None, -(s.get("grade") or 0)))
        return sorted(self.students, key=lambda s: s.get("name", "").lower())

    def stats_by_major(self) -> Dict[str, Dict]:
        from collections import defaultdict
        d = defaultdict(list)
        for s in self.students:
            d[s.get("major", "Unknown")].append(s.get("grade"))

        stats = {}
        for major, grades in d.items():
            nums = [g for g in grades if isinstance(g, int)]
            count = len(grades)
            avg = sum(nums) / len(nums) if nums else None
            stats[major] = {"count": count,
                            "grades_assigned": len(nums), "avg": avg}
        return stats
