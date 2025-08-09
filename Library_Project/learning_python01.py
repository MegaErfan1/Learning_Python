import json
import os


class Library():
    def __init__(self, filename="data/Books.json"):
        self.filename = filename
        self.books = []
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.mkdir(folder)
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.books = json.load(f)
        else:
            self.books = []

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def add_book(self, id_book, title, copies=1):
        if not id_book.strip():
            print("❌ Book ID cannot be empty!")
            return
        for b in self.books:
            if b["id_book"] == id_book:
                print(f'{b["title"]} already been added.')
                return
        self.books.append({
            "id_book": id_book,
            "title": title,
            "copies": copies
        })
        self.save_data()

    def bring_book(self, id_book):
        for t in self.books:
            if t["id_book"] == id_book:
                t["copies"] += 1
                print(f"You delivered {t['title']}.")
                self.save_data()
                return
        print("This book is not ours.")

    def get_book(self, id_book):
        for t in self.books:
            if t["id_book"] == id_book:
                if t["copies"] > 0:
                    t["copies"] -= 1
                    print(f"You received {t['title']}.")
                    self.save_data()
                else:
                    print(f"No copies of {t['title']} are available.")
                return
        print("This book is not ours.")

    def show_books(self):
        for b in self.books:
            print({
                "id_book": b["id_book"],
                "title": b["title"],
                "copies": b["copies"]
            })
