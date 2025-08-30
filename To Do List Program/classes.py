import csv
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Style


class Task:
    def __init__(self, name, description, priority, due_date=None, status="not done"):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date

    def mark_done(self):
        self.status = "Done"

    def __str__(self):
        return f"{self.name} ({self.priority}) - {self.description} | {self.status} | {self.due_date or '---'}"


class ToDoList:
    def __init__(self, filename="tasks.csv"):
        self.filename = filename
        self.tasks = []
        self.load_from_csv()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_to_csv()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_to_csv()
            return True
        return False

    def mark_task_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_done()
            self.save_to_csv()
            return True
        return False

    def show_tasks(self):
        if not self.tasks:
            print("No tasks have been registered.")
            return

        table = PrettyTable()
        table.field_names = ["#", "name", "discription",
                             "priority", "status", "due date"]

        for i, task in enumerate(self.tasks, start=1):
            priority_color = task.priority
            if task.priority == "High":
                priority_color = Fore.RED + task.priority + Style.RESET_ALL
            elif task.priority == "Medium":
                priority_color = Fore.YELLOW + task.priority + Style.RESET_ALL
            else:
                priority_color = Fore.GREEN + task.priority + Style.RESET_ALL

            table.add_row([i, task.name, task.description,
                          priority_color, task.status, task.due_date or "---"])

        print(table)

    def search_task(self, keyword):
        return [t for t in self.tasks if keyword in t.name or keyword in t.description]

    def filter_tasks(self, priority=None, status=None):
        results = self.tasks
        if priority:
            results = [t for t in results if t.priority == priority]
        if status:
            results = [t for t in results if t.status == status]
        return results

    def sort_tasks(self, by="priority"):
        if by == "priority":
            order = {"High": 1, "Medium": 2, "Low": 3}
            self.tasks.sort(key=lambda x: order.get(x.priority, 99))
        elif by == "due_date":
            self.tasks.sort(key=lambda x: datetime.strptime(
                x.due_date, "%Y-%m-%d") if x.due_date else datetime.max)

    def save_to_csv(self):
        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["name", "description", "priority", "status", "due_date"])
            for task in self.tasks:
                writer.writerow([task.name, task.description,
                                task.priority, task.status, task.due_date])

    def load_from_csv(self):
        try:
            with open(self.filename, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    task = Task(
                        row["name"],
                        row["description"],
                        row["priority"],
                        row["due_date"] if row["due_date"] else None,
                        row["status"]
                    )
                    self.tasks.append(task)
        except FileNotFoundError:
            open(self.filename, "w", encoding="utf-8").close()
