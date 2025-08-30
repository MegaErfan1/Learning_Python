# ToDo List (Python CLI)

A simple command-line program for managing your task list.  
Main features:

- Add new tasks ✅
- Delete tasks ❌
- Show all tasks 📋
- Mark tasks as done 🔄
- Search in tasks 🔍
- Filter tasks 🎯
- Sort by priority or due date 📅
- Auto save & load tasks from `tasks.csv` 💾

---

## Files
- `classes.py` → contains `Task` and `ToDoList` classes
- `main.py` → main menu and user interaction

---
Important Note 
To get better results when entering Priority,
use strip() and capitalize() to normalize user input:
    priority = input("Priority (High/Medium/Low): ").strip().capitalize()
This way, no matter if you type high, HIGH, or hIgH,
it will always be stored as High.

-MegaErfan