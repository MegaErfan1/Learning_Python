from learning_python01 import Library


def ask_menu():
    choice = input("\nDo you want to go back to menu? (Y/N): ").strip().lower()
    if choice not in ("y", "yes"):
        print("Thank you for visiting my Library, Goodbye!")
        exit()


def main():
    Lib = Library()

    while True:
        print("\nWelcome To My Library")
        print("___Library`s Menu___")
        print("1. Add Book ")
        print("2. Bring Book")
        print("3. Get Book")
        print("4. Show All Books")
        print("5. Exit")

        choice = input("Enter Your choice: ").strip()

        if choice == "1":
            title = input("Enter Book Name: ").strip()
            id_book = ""
            while not id_book.strip():
                id_book = input("Enter ID-Book: ").strip()
                if not id_book:
                    print("❌ ID cannot be empty!")

            copies = input("How many Copies do you add? ").strip()
            if not copies.isdigit():
                copies = 1
            else:
                copies = int(copies)

            Lib.add_book(id_book, title, copies)
            ask_menu()

        elif choice == "2":
            id_book = input("Enter ID-Book: ").strip()
            Lib.bring_book(id_book)
            ask_menu()

        elif choice == "3":
            id_book = input("Enter ID-Book: ").strip()
            Lib.get_book(id_book)
            ask_menu()

        elif choice == "4":
            Lib.show_books()
            ask_menu()

        elif choice == "5":
            print("Thank you for visiting my Library, Goodbye!")
            break

        else:
            print("Invalid choice, Try Again")


if __name__ == "__main__":
    main()
