import unittest.mock
from unittest import TestCase
from unittest.mock import patch, MagicMock

from main import MainApplication


class TestMainApplicationFunctions(TestCase):
    @patch('main.Library')
    def test_book_ids_correctly_initialized(self, mock_library):
        # Setup mock library to return a predefined list of books
        mock_books = [
            {'uuid': 'uuid1', 'title': 'Book One', 'author': 'Author One', 'available': True},
            {'uuid': 'uuid2', 'title': 'Book Two', 'author': 'Author Two', 'available': False}
        ]
        mock_library_instance = MagicMock()
        mock_library_instance.bList = mock_books
        mock_library.return_value = mock_library_instance

        # Instantiate MainApplication and check bookIDs
        app = MainApplication()
        expected_book_ids = {1: 'uuid1', 2: 'uuid2'}

        self.assertEqual(app.bookIDs, expected_book_ids)

    @patch('main.Library')
    @patch('main.Printer')
    def test_display_menu_shows_correct_options(self, mock_printer, *args, **kwargs):
        app = MainApplication()
        app.display_menu()

        # Expected menu options
        expected_calls = [
            ('1. Display Books',),
            ('2. Issue Book',),
            ('3. Return Book',),
            ('4. Add Book',),
            ('5. Search Book',),
            ('6. Remove Book',),
            ('7. Display Outdated Issued Books',),
            ('8. Clear console',),
            ('9. Exit',)
        ]

        # Verify each expected call was made to Printer.print
        mock_printer.return_value.print.assert_has_calls([unittest.mock.call(*args) for args in expected_calls],
                                                         any_order=False)


class MainApplicationMethodsSetup:
    def setUp(self):
        self.printer = MagicMock()
        self.library = MagicMock()
        self.library.bList = [
            {'uuid': 'uuid1', 'title': 'Book One', 'author': 'Author One', 'available': True},
            {'uuid': 'uuid2', 'title': 'Book Two', 'author': 'Author Two', 'available': False},
            {'uuid': 'uuid3', 'title': 'Book Three', 'author': 'Author Three', 'available': True},
        ]


class TestMainApplicationDisplayBooksMethod(MainApplicationMethodsSetup, TestCase):

    @patch('main.Library')
    @patch('main.Printer')
    def test_no_books_found_message(self, mock_printer, mock_library):
        # Setup mock library to return an empty list of books
        mock_library_instance = MagicMock()
        mock_library_instance.bList = []
        mock_library.return_value = mock_library_instance

        app = MainApplication()
        app.display_books()

        # Verify Printer.error was called with the expected message
        mock_printer.return_value.error.assert_called_once_with('No books found!')

    @patch('main.Library')
    @patch('main.Printer')
    def test_books_found_are_displayed_correctly(self, mock_printer, mock_library):
        # Setup mock library to return a predefined list of books
        mock_library.return_value = self.library

        app = MainApplication()
        app.display_books()

        # Expected calls to Printer.print
        expected_calls = [
            ('Book 1:',),
            ('Book 2:',),
        ]
        mock_printer.return_value.print.assert_has_calls([unittest.mock.call(*args) for args in expected_calls])


class TestMainApplicationIssueBookMethod(MainApplicationMethodsSetup, TestCase):
    @patch('main.Printer.input', return_value=1)
    @patch('main.Library')
    def test_issue_book_calls_correct_library_method(self, mock_library, mock_printer):
        mock_library.return_value = self.library
        app = MainApplication()
        app.issue_book()

        # Verify Library.issue_book was called with the correct UUID
        mock_library.return_value.issue_book.assert_called_once_with('uuid1')


class TestMainApplicationReturnBookMethod(MainApplicationMethodsSetup, TestCase):
    @patch('main.Printer.input', return_value=1)
    @patch('main.Library')
    def test_return_book_calls_correct_library_method(self, mock_library, mock_printer):
        mock_library.return_value = self.library
        app = MainApplication()
        app.return_book()

        # Verify Library.return_book was called with the correct UUID
        mock_library.return_value.return_book.assert_called_once_with('uuid1')


class TestMainApplicationAddBookMethod(MainApplicationMethodsSetup, TestCase):
    @patch('main.Printer')
    @patch('main.Library')
    def test_add_book_calls_correct_library_method(self, mock_library, mock_printer):
        self.printer.input.side_effect = ['Test Author', 'Test Title']
        mock_printer.return_value = self.printer
        mock_library.return_value = self.library
        app = MainApplication()
        app.add_book()

        # Verify Library.add_book was called with the correct book title
        mock_library.return_value.add_book.assert_called_once_with('Test Author', 'Test Title')


class TestMainApplicationSearchBookMethod(MainApplicationMethodsSetup, TestCase):
    def setUp(self):
        super().setUp()
        self.printer.input.side_effect = ['title', 'Book One']

    @patch('main.Printer')
    @patch('main.Library')
    def test_search_book_calls_search_by_method(self, mock_library, mock_printer):
        mock_printer.return_value = self.printer
        mock_library.return_value = self.library
        app = MainApplication()
        app.search_book()

        # Verify Library.search_by was called with the correct attribute and value
        mock_library.return_value.search_by.assert_called_once_with('title', 'Book One')

    @patch('main.Printer')
    @patch('main.Library')
    def test_search_book_calls_display_book_method(self, mock_library, mock_printer):
        self.library.search_by.return_value = ['uuid1']
        mock_printer.return_value = self.printer
        mock_library.return_value = self.library
        app = MainApplication()
        app.search_book()

        mock_library.return_value.display_book.assert_called_once_with('uuid1')


class TestMainApplicationRemoveBookMethod(MainApplicationMethodsSetup, TestCase):
    @patch('main.Printer.input', return_value=1)
    @patch('main.Library')
    def test_remove_book_calls_correct_library_method(self, mock_library, mock_printer):
        mock_library.return_value = self.library
        app = MainApplication()
        app.remove_book()

        # Verify Library.display_book was called with the correct UUID
        mock_library.return_value.display_book.assert_called_once_with('uuid1')

    @patch('main.Printer')
    @patch('main.Library')
    def test_remove_book_confirms_deletion(self, mock_library, mock_printer):
        self.printer.input.side_effect = [1, 'y']
        mock_printer.return_value = self.printer
        mock_library.return_value = self.library
        app = MainApplication()
        app.remove_book()

        # Verify Library.remove_book was called with the correct UUID
        mock_library.return_value.remove_book.assert_called_once_with('uuid1')

    @patch('main.Printer')
    @patch('main.Library')
    def test_remove_book_cancels_deletion(self, mock_library, mock_printer):
        self.printer.input.side_effect = [1, 'n']
        mock_printer.return_value = self.printer
        mock_library.return_value = self.library
        app = MainApplication()
        app.remove_book()

        # Verify Library.remove_book was not called
        mock_library.return_value.remove_book.assert_not_called()


class TestMainApplicationDisplayOutdatedIssuedBooksMethod(MainApplicationMethodsSetup, TestCase):
    @patch('main.Library')
    @patch('main.Printer')
    def test_no_outdated_books_found_message(self, mock_printer, mock_library):
        # Setup mock library to return a list of books without any outdated books
        self.library.bList = [
            {'uuid': 'uuid1', 'title': 'Book One', 'author': 'Author One', 'available': False,
             'expire_date': '2097/12/31 00:00:00'},
            {'uuid': 'uuid2', 'title': 'Book Two', 'author': 'Author Two', 'available': False,
             'expire_date': '2092/12/31 00:00:00'}
        ]
        mock_library.return_value = self.library

        app = MainApplication()
        app.display_outdated_issued_books()

        # Verify Printer.print was called with the expected message
        mock_printer.return_value.print.assert_called_once_with('No outdated books found!')

    @patch('main.Library')
    @patch('main.Printer')
    def test_outdated_books_are_displayed_correctly(self, mock_printer, mock_library):
        # Setup mock library to return a list of books with an outdated book
        self.library.bList = [
            {'uuid': 'uuid1', 'title': 'Book One', 'author': 'Author One', 'available': False,
             'expire_date': '1337/12/31 00:00:00'},
            {'uuid': 'uuid2', 'title': 'Book Two', 'author': 'Author Two', 'available': False,
             'expire_date': '2000/12/31 00:00:00'}
        ]
        mock_library.return_value = self.library

        app = MainApplication()
        app.display_outdated_issued_books()

        # Expected calls to Printer.print
        expected_calls = [
            ('Book uuid1 is outdated!',),
            ('Book uuid2 is outdated!',),
        ]
        mock_printer.return_value.print.assert_has_calls([unittest.mock.call(*args) for args in expected_calls])


class TestMainApplicationExitApplicationMethod(MainApplicationMethodsSetup, TestCase):
    @patch('main.Printer')
    @patch('main.Library')
    def test_exit_application_calls_library_save_method(self, mock_library, mock_printer):
        self.printer.input.side_effect = ['y', 'json']
        mock_printer.return_value = self.printer
        mock_library.return_value = self.library
        app = MainApplication()
        app.exit_application()

        mock_library.return_value.save.assert_called_once_with('json')


if __name__ == '__main__':
    unittest.main()
