import os
from typing import TypedDict, Optional, Callable, Any


class Book(TypedDict):
    uuid: str
    name: str
    author: str
    available: bool
    issue_date: str
    expire_date: str
    number_of_readings: int


class Printer:
    """
    A utility class for printing messages with indentation.

    Attributes:
        tab_count (int): The number of tabs to prepend to the message.
    """

    instance = None
    _initialized = False

    def __new__(cls):
        """
        Singleton implementation.
        """
        if cls.instance is None:
            cls.instance = super(Printer, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """
        Initializes the tab count to zero.
        """
        if not self._initialized:
            self._initialized = True
            self.tab_count = 0

    def __enter__(self):
        """
        Increases the tab count by one when entering the context.
        """
        self.tab_count += 1
        return self

    def __exit__(self, *args, **kwargs):
        """
        Decreases the tab count by one when exiting the context.
        """
        self.tab_count -= 1
        return False

    def format(self, string):
        """
        Prints a message with the current number of tabs prepended.

        Args:
            string (str): The message to print.
        """
        return self.tab_count * '\t' + string

    def print(self, msg, *args, **kwargs):
        """
        Prints a message with the current number of tabs prepended.

        Args:
            msg (str): The message to print.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        print(self.format("[+] " + msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Prints an error message with the current number of tabs prepended.

        Args:
            msg (str): The message to print.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        print(self.format("[-] " + msg), *args, **kwargs)

    def input(self, message, validation_function: Optional[Callable[[str], Optional[Any]]] = None, counter: int = 3):
        """
        Prints a message with the current number of tabs prepended.
        Prompts the user for input and validates it.

        Args:
            message (str): The prompt message.
            validation_function (function, optional): A function to validate the input. Defaults to None.
        Returns:
            The validated input.
        """
        while counter:
            answer = input(self.format("[*] " + message))
            if answer:
                if validation_function is not None:
                    if (result := validation_function(answer)) is not None:
                        return result
                    else:
                        continue
                return answer
            counter -= 1
        else:
            self.error("Too many attempts!")
            raise InterruptedError

    @staticmethod
    def clear():
        """
        Clears the console screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')


def validate_integer(string: str) -> int | None:
    """
    Validates if a string can be converted to an integer.

    Args:
        string (str): The string to validate.

    Returns:
        int: The converted integer if valid, None otherwise.
    """
    printer = Printer()
    try:
        return int(string)
    except ValueError:
        printer.error(f"{string} is not integer!")
        return None


def validate_book_attributes(string: str) -> str | None:
    """
    Validates if a string is a valid book attribute.

    Args:
        string (str): The string to validate.

    Returns:
        str: The validated string if valid, None otherwise.
    """
    attributes = [
        "name", "author", "available", "issue_date", "expire_date", "number_of_readings", "uuid"
    ]
    printer = Printer()
    if string.lower() in attributes:
        return string
    else:
        printer.error(f'Invalid attribute! Please select one of attributes: {", ".join(attributes)}')


def list2dict(data: list[Book]) -> dict[str, Book]:
    """
    Converts a list of books to a dictionary where the keys are the UUIDs of the books.

    Args:
        data (list[Book]): A list of books, where each book is a dictionary with 'uuid' as one of the keys.

    Returns:
        dict[str, Book]: A dictionary where the keys are the UUIDs of the books and the values are the books themselves.
    """
    result_dict = {}
    for i, item in enumerate(data):
        new_item = {**item}
        uuid = new_item.pop('uuid') if 'uuid' in new_item.keys() else str(i)
        result_dict[uuid] = new_item
    return result_dict


def dict2list(book: dict[str, Book]) -> list[Book]:
    """
    Converts a dictionary of books to a list of books.

    Args:
        book (dict[str, Book]): A dictionary where the keys are the UUIDs of the books and the values are the books themselves.

    Returns:
        list[Book]: A list of books, where each book is a dictionary with 'uuid' as one of the keys.
    """
    result_list = []
    for uuid, item in book.items():
        item['uuid'] = uuid
        result_list.append(item)

    return result_list
