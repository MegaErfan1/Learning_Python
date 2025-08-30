from classes import Task, ToDoList


def main_menu():
    todo = ToDoList()

    while True:
        print("\n=========Task List Management=========")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Show All Tasks")
        print("4. Change the status of the task to completed")
        print("5. Search In Tasks")
        print("6. Filtering Tasks")
        print("7. Sorting Tasks")
        print("8. Exit")
        print("====================================")

        choice = input("Your Choice: ")

        if choice == "1":
            name = input("Task Name: ")
            description = input("Description: ")
            priority = input("Priority(High/Medium/Low): ")
            due_date = input("Due date (YYYY-MM-DD or empty)") or None
            task = Task(name, description, priority, due_date)
            todo.add_task(task)
            print("Task Added.")

        elif choice == "2":
            todo.show_tasks()
            try:
                idx = int(input("Task number to delete: ")) - 1
                if todo.remove_task(idx):
                    print("The task has been deleted.")
                else:
                    print("Invalid Number")
            except ValueError:
                print("Please Enter A Number.")

        elif choice == "3":
            todo.show_tasks()

        elif choice == "4":
            todo.show_tasks()
            try:
                idx = int(input("Task number to change status: ")) - 1
                if todo.mark_task_done(idx):
                    print("The status of the task has been changed.")
                else:
                    print("Invalid Number")
            except ValueError:
                print("Please Enter A Number")

        elif choice == "5":
            keyword = input("Word To Search: ")
            results = todo.search_task(keyword)
            if results:
                for r in results:
                    print(r)
            else:
                print("No Results Found.")

        elif choice == "6":
            p = input("Priority filter (High/Medium/Low or empty): ") or None
            s = input("Filter status (ِDone/Not Done or empty): ") or None
            results = todo.filter_tasks(p, s)
            if results:
                for r in results:
                    print(r)
            else:
                print("No Results Found.")

        elif choice == "7":
            by = input("Sorting by (priority/due_date): ").strip()
            todo.sort_tasks(by)
            print("Sorted.")
            todo.show_tasks()

        elif choice == "8":
            print("Save and exit.")
            todo.save_to_csv()
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main_menu()
