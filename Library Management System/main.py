from os.path import join as join_path

from managers.library import Library
from utils import validate_integer, Printer

"""
Analyzing the code,
The project file structure is as follows:
    .
    ├── main.py
    ├── managers
    │   ├── loaders.py
    │   └── library.py
    ├── resources
    │   └── books.json
    └── utils.py
"""

class MainApplication:
    def __init__(self, fileName: str = join_path('resources', 'books.json')):
        self.library = Library(bookListFile=fileName)
        self.printer = Printer()

    @property
    def bookIDs(self):
        return {(i + 1): b['uuid'] for i, b in enumerate(self.library.bList)}

    def __call__(self):
        while True:
            self.display_menu()
            choice = self.printer.input("Enter your choice: ", validate_integer, 9999)
            try:
                match choice:
                    case 1:
                        self.display_books()
                    case 2:
                        self.issue_book()
                    case 3:
                        self.return_book()
                    case 4:
                        self.add_book()
                    case 5:
                        self.search_book()
                    case 6:
                        self.remove_book()
                    case 7:
                        self.display_outdated_issued_books()
                    case 8:
                        self.clear_console()
                    case 9:
                        if self.exit_application():
                            break
                    case _:
                        self.invalid_choice()
            except KeyboardInterrupt:
                self.printer.error("Exiting...")
                break
            except InterruptedError:
                continue
            except Exception as e:
                self.printer.error(f"An error occurred: {e}")

    def display_menu(self):
        self.printer.print("1. Display Books")
        self.printer.print("2. Issue Book")
        self.printer.print("3. Return Book")
        self.printer.print("4. Add Book")
        self.printer.print("5. Search Book")
        self.printer.print("6. Remove Book")
        self.printer.print("7. Display Outdated Issued Books")
        self.printer.print("8. Clear console")
        self.printer.print("9. Exit")

    def display_books(self):
        if len(self.bookIDs) != 0:
            for id, uuid in self.bookIDs.items():
                self.printer.print(f"Book {id}:")
                with self.printer:
                    self.library.display_book(uuid)
        else:
            self.printer.error("No books found!")

    def issue_book(self):
        uuid = self.bookIDs[self.printer.input("Enter the ID of the book you want to issue: ",
                                               lambda s: i if (i := validate_integer(s)) in self.bookIDs else None)]
        self.library.issue_book(uuid)

    def return_book(self):
        uuid = self.bookIDs[self.printer.input("Enter the ID of the book you want to return: ",
                                               lambda s: i if (i := validate_integer(s)) in self.bookIDs else None)]
        self.library.return_book(uuid)

    def add_book(self):
        title = self.printer.input("Enter the title of the book: ")
        author = self.printer.input("Enter the author of the book: ")
        self.library.add_book(title, author)

    def search_book(self):
        # TODO: Implement search functionality
        # 1. Ask the user for the attribute to search by
        # 2. Ask the user for the value of the attribute
        # 3. Call the search_by method of the library instance
        # 4. Display the books that match the search
        pass

    def remove_book(self):
        # TODO: Implement remove functionality
        # 1. Ask the user for the ID of the book to remove
        # 2. Display the book details
        # 3. Ask the user for confirmation
        # 4. Call the remove_book method of the library instance
        pass

    def display_outdated_issued_books(self):
        # TODO: Implement display_outdated_issued_books functionality
        # 1. Compare expire_date with the current date
        # 2. Display the details of the outdated books
        # 3. Display message if no book outdated
        pass

    def clear_console(self):
        self.printer.clear()

    def exit_application(self):
        yes = self.printer.input("Do you want to save the changes? (y/n): ",
                                 lambda s: s.lower() if s.lower() in ["y", "n"] else None)
        if yes == "y":
            save_format = self.printer.input("Enter the format to save the changes (e.g., json, xml): ")
            return self.library.save(save_format)
        return True

    def invalid_choice(self):
        self.printer.error("Invalid choice! Please try again.")


if __name__ == "__main__":
    app = MainApplication()
    app()
