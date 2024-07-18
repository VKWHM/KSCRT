import datetime
import uuid as _uuid

from managers.loaders import get_loader, dump_data
from utils import Printer, Book


class Library:
    """
    This class represents a library, which manages a collection of books.

    Attributes:
        lName (str): The name of the library.
        dataLoader (FileLoader): The file loader used to load and save the book list.
        bookListFile (str): The path of the file containing the book list.
        bList (list[Book]): A list of books in the library.
        _printer (Printer): A printer used to print messages.
    """

    def __init__(self, libraryName: str = "Library", bookListFile: str = "books.json"):
        """
        Initializes a new instance of the Library class.

        Args:
            libraryName (str): The name of the library.
            bookListFile (str): The path of the file containing the book list.
        """
        self.lName = libraryName
        dataLoaderClass = get_loader(bookListFile)
        self.dataLoader = dataLoaderClass[list[Book]](bookListFile)
        self.bookListFile = bookListFile
        self.bList = self.dataLoader.load()
        self._printer = Printer()

    def _get_book(self, uuid):
        return next((book for book in self.bList if book["uuid"] == uuid), None)

    def display_book(self, uuid: str) -> None:
        """
        Displays the details of a book.

        Args:
            uuid (str): The UUID of the book to display.
        """

        book = self._get_book(uuid)
        if book:
            self._print_book(book)
        else:
            self._printer.error("Book with UUID {} not found.".format(uuid))

    def issue_book(self, uuid: str) -> None:
        """
        Displays the details of a book.

        Args:
            uuid (str): The UUID of the book to display.
        """

        book = self._get_book(uuid)
        with self._printer as p:
            if book:
                if book["available"]:
                    book["available"] = False
                    book["issue_date"] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    book["expire_date"] = (datetime.datetime.now() + datetime.timedelta(weeks=4)).strftime(
                        "%Y/%m/%d %H:%M:%S")
                    book["number_of_readings"] += 1
                    p.print("Book issued successfully!")
                else:
                    p.error(
                        "This book is already issued. Issue Date: {}; Expire Date: {}".format(book["issue_date"],
                                                                                              book["expire_date"]))
            else:
                p.error("Invalid UUID!")

    def return_book(self, uuid: str) -> None:
        """
        Returns a book.

        Args:
            uuid (str): The UUID of the book to return.
        """

        with self._printer as p:
            book = self._get_book(uuid)
            if book:
                if not book["available"]:
                    book["available"] = True
                    book["issue_date"] = ""
                    book["expire_date"] = ""
                    p.print("Book returned successfully!")
                else:
                    p.error("This book is not issued.")
            else:
                p.error("Invalid UUID!")

    def add_book(self, title: str, author: str) -> None:
        """
        Adds a book to the library.
        """
        uuid = str(_uuid.uuid4())
        book = Book(
            uuid=uuid,
            name=title,
            author=author,
            available=True,
            issue_date="",
            expire_date="",
            number_of_readings=0
        )
        self.bList.append(book)
        with self._printer as p:
            p.print("Book added successfully!")
            self._print_book(book)

    def search_by(self, attribute: str, value: str) -> list[str] | None:
        """
        Searches for books by a specific attribute.

        Args:
            attribute (str): The attribute to search by.
            value (str): The value of the attribute to search for.

        Returns:
            list[str] | None: A list of UUIDs of the books that match the search, or None if no books were found.
        """
        results = []
        if len(self.bList) != 0:
            book = self.bList[0]
            if attribute in book:
                if isinstance(book[attribute], str):
                    for book in self.bList:
                        if book[attribute].lower() == value.lower():
                            results.append(book["uuid"])
                elif isinstance(book[attribute], bool):
                    for book in self.bList:
                        if book[attribute] == (value.lower() == 'true'):
                            results.append(book["uuid"])
                elif isinstance(book[attribute], int):
                    for book in self.bList:
                        if book[attribute] == int(value):
                            results.append(book["uuid"])
                else:
                    raise ValueError(f"Unsupported attribute type: {type(book[attribute])}")

        if results:
            return results
        else:
            with self._printer as p:
                p.error("No books found with {}: {}".format(attribute, value))
                return None

    def _print_book(self, book: Book) -> None:
        """
        Prints the details of a book.

        Args:
            book (Book): The book to print.
        """
        self._printer.print(f"UUID: {book['uuid']}")
        self._printer.print(f"Name: {book['name']}")
        self._printer.print(f"Author: {book['author']}")
        self._printer.print(f"Available: {book['available']}")
        self._printer.print(f"Issue Date: {book['issue_date']}")
        self._printer.print(f"Expire Date: {book['expire_date']}")
        self._printer.print(f"Number of Readings: {book['number_of_readings']}\n")

    def remove_book(self, uuid: str) -> None:
        """
        Removes a book from the library.

        Args:
            uuid (str): The UUID of the book to remove.
        """
        book = self._get_book(uuid)
        with self._printer as p:
            if book:
                self.bList.remove(book)
                p.print("Book removed successfully!")
            else:
                p.error("Invalid UUID!")

    def save(self, save_format: str) -> bool:
        """
        Saves the book list to a file.

        Args:
            save_format (str): The format to save the book list in.
        """
        try:
            if self.dataLoader.fileExt != save_format:
                dump_data(self.bList, f"{self.dataLoader.fileName}.{save_format}")
            self.dataLoader.save(self.bList)
            with self._printer as p:
                p.print("Changes saved successfully!")
                return True
        except KeyboardInterrupt:
            self._printer.error(f"File format {save_format} is unsupported!")
            return False
