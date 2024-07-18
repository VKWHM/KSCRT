from datetime import datetime
from os.path import join as join_path

from managers.library import Library
from utils import validate_integer, validate_book_attributes, Printer


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
        attribute = self.printer.input("Enter the attribute to search by (e.g., name, author, available): ",
                                       validate_book_attributes)
        value = self.printer.input(f"Enter the value for {attribute}: ")
        uuids = self.library.search_by(attribute, value)
        if uuids:
            for id, uuid in self.bookIDs.items():
                if uuid in uuids:
                    self.printer.print(f"Book {id}:")
                    with self.printer:
                        self.library.display_book(uuid)
        else:
            self.printer.error("No books found!")

    def remove_book(self):
        uuid = self.bookIDs[self.printer.input("Enter the ID of the book you want to remove: ",
                                               lambda s: i if (i := validate_integer(s)) in self.bookIDs else None)]
        self.library.display_book(uuid)
        answer = self.printer.input("Are you sure you want to remove this book? (y/n): ",
                                    lambda s: s.lower() if s.lower() in ["y", "n"] else None)
        if answer == "y":
            self.library.remove_book(uuid)
        else:
            self.printer.print("Book was not removed.")

    def display_outdated_issued_books(self):
        today = datetime.now()
        has_outdated_books = False
        for book in self.library.bList:
            if not book['available'] and datetime.strptime(book['expire_date'], "%Y/%m/%d %H:%M:%S") < today:
                if not has_outdated_books:
                    has_outdated_books = True
                self.printer.print(f"Book {book['uuid']} is outdated!")
                with self.printer:
                    self.library.display_book(book['uuid'])
        if not has_outdated_books:
            self.printer.print("No outdated books found!")

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