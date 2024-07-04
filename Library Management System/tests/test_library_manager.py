import os
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from managers.library import Library
from utils import Printer

test_samples = """[
    {
        "uuid": "03d462ed-dbac-43b4-8a66-c3cfaf47245a",
        "name": "The Hitchhiker's Guide To The Galaxy",
        "author": "Douglas Adams",
        "available": false,
        "issue_date": "2024/06/26 16:55:12",
        "expire_date": "2024/07/09 16:55:12",
        "number_of_readings": 17
    },
    {
        "uuid": "f07abcb2-1f4b-457b-a856-cdff22f7acfc",
        "name": "Watership Down",
        "author": "Richard Adams",
        "available": true,
        "issue_date": null,
        "expire_date": null,
        "number_of_readings": 51
    },
    {
        "uuid": "a74e8e90-2b3b-4c53-a166-8dfb3b2783b1",
        "name": "The Five People You Meet in Heaven",
        "author": "Mitch Albom",
        "available": true,
        "issue_date": null,
        "expire_date": null,
        "number_of_readings": 75
    },
    {
        "uuid": "d5feecd6-b41a-4d6e-bd7a-ad8eeed5b5bf",
        "name": "Speak",
        "author": "Laurie Halse Anderson",
        "available": true,
        "issue_date": null,
        "expire_date": null,
        "number_of_readings": 5
    },
    {
        "uuid": "d09d6221-dd8f-4667-a4e9-2f063ee37f5d",
        "name": "I Know Why the Caged Bird Sings",
        "author": "Maya Angelou",
        "available": true,
        "issue_date": null,
        "expire_date": null,
        "number_of_readings": 74
    }
]"""


class LibraryManagerTests(unittest.TestCase):
    def setUp(self):
        self.test_file_path = "test_books.json"
        with open(self.test_file_path, 'w') as f:
            f.write(test_samples)

    def test_library_manager_init_method(self):
        library = Library(bookListFile=self.test_file_path)
        self.assertEqual(library.lName, "Library")
        self.assertEqual(library.bookListFile, self.test_file_path)
        self.assertEqual(len(library.bList), 5)
        self.assertIsInstance(library._printer, Printer)

    def test_library_manager_display_book_method(self):
        with patch.object(Library, "_print_book") as mock_print_book:
            library = Library(bookListFile=self.test_file_path)
            library.display_book("d09d6221-dd8f-4667-a4e9-2f063ee37f5d")
            self.assertTrue(mock_print_book.called)

    @patch('datetime.datetime')
    @patch('datetime.timedelta')
    def test_library_manager_issue_book_method(self, mock_timedelta, mock_datetime):
        now = datetime(2024, 7, 3, 12, 0, 0)  # Use a fixed date for consistency
        now_str = now.strftime("%Y/%m/%d %H:%M:%S")

        mock_datetime.now.return_value = now
        mock_timedelta.return_value = timedelta(weeks=4)

        library = Library(bookListFile=self.test_file_path)
        library.issue_book("d09d6221-dd8f-4667-a4e9-2f063ee37f5d")
        book = library._get_book("d09d6221-dd8f-4667-a4e9-2f063ee37f5d")

        self.assertFalse(book["available"])
        self.assertEqual(book["issue_date"], now.strftime("%Y/%m/%d %H:%M:%S"))
        self.assertEqual(book["expire_date"], (now + timedelta(weeks=4)).strftime("%Y/%m/%d %H:%M:%S"))

    def test_library_manager_return_book_method(self):
        library = Library(bookListFile=self.test_file_path)
        library.return_book("03d462ed-dbac-43b4-8a66-c3cfaf47245a")
        book = library._get_book("03d462ed-dbac-43b4-8a66-c3cfaf47245a")

        self.assertTrue(book["available"])
        self.assertEqual(book["issue_date"], '')
        self.assertEqual(book["expire_date"], '')

    def test_library_manager_add_book_method(self):
        library = Library(bookListFile=self.test_file_path)
        library.add_book("New Book", "New Author")
        self.assertEqual(len(library.bList), 6)
        self.assertEqual(library.bList[-1]["name"], "New Book")
        self.assertEqual(library.bList[-1]["author"], "New Author")

    def test_library_manager_search_by_method(self):
        library = Library(bookListFile=self.test_file_path)
        search_keys_values = (
            ("name", "The Five People You Meet in Heaven", ["a74e8e90-2b3b-4c53-a166-8dfb3b2783b1"]),
            ("author", "Mitch Albom", ["a74e8e90-2b3b-4c53-a166-8dfb3b2783b1"]),
            ("available", 'True', ["f07abcb2-1f4b-457b-a856-cdff22f7acfc", "a74e8e90-2b3b-4c53-a166-8dfb3b2783b1",
                                   "d5feecd6-b41a-4d6e-bd7a-ad8eeed5b5bf", "d09d6221-dd8f-4667-a4e9-2f063ee37f5d"]),
            ("available", 'False', ["03d462ed-dbac-43b4-8a66-c3cfaf47245a"]),
        )
        for key, value, correct_uuids in search_keys_values:
            with self.subTest(msg=f"Searching by {key}={value}"):
                uuids = library.search_by(key, value)
                self.assertTrue(uuids == correct_uuids)

    def test_library_manager_remove_book_method(self):
        library = Library(bookListFile=self.test_file_path)
        library.remove_book("d09d6221-dd8f-4667-a4e9-2f063ee37f5d")
        self.assertEqual(len(library.bList), 4)
        self.assertNotIn("d09d6221-dd8f-4667-a4e9-2f063ee37f5d", [book["uuid"] for book in library.bList])

    def tearDown(self):
        os.remove(self.test_file_path)
