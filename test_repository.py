import unittest
import sqlite3
from repository import LibraryRepository


class TestLibraryRepository(unittest.TestCase):
    def setUp(self):
        # in-memory DB — fresh for every test, no file left behind
        self.repo = LibraryRepository(":memory:")

    def tearDown(self):
        self.repo.close()

    def test_add_and_get_book(self):
        self.repo.add_book('Clean Code', 'B001', 'Robert Martin', 'Available', 'N/A')
        book = self.repo.get_book('B001')
        self.assertEqual(book, ('Clean Code', 'B001', 'Robert Martin', 'Available', 'N/A'))

    def test_add_duplicate_id_raises(self):
        self.repo.add_book('Clean Code', 'B001', 'Robert Martin', 'Available', 'N/A')
        with self.assertRaises(sqlite3.IntegrityError):
            self.repo.add_book('Refactoring', 'B001', 'Martin Fowler', 'Available', 'N/A')

    def test_get_all_books(self):
        self.repo.add_book('Clean Code', 'B001', 'Robert Martin', 'Available', 'N/A')
        self.repo.add_book('Refactoring', 'B002', 'Martin Fowler', 'Available', 'N/A')
        self.assertEqual(len(self.repo.get_all_books()), 2)

    def test_update_book(self):
        self.repo.add_book('Clean Code', 'B001', 'Robert Martin', 'Available', 'N/A')
        self.repo.update_book('B001', 'Clean Code (2nd Ed)', 'Available', 'Robert Martin', 'N/A')
        book = self.repo.get_book('B001')
        self.assertEqual(book[0], 'Clean Code (2nd Ed)')

    def test_update_status_to_issued(self):
        self.repo.add_book('Clean Code', 'B001', 'Robert Martin', 'Available', 'N/A')
        self.repo.update_status('B001', 'Issued', 'CARD123')
        book = self.repo.get_book('B001')
        self.assertEqual(book[3], 'Issued')
        self.assertEqual(book[4], 'CARD123')

    def test_delete_book(self):
        self.repo.add_book('Clean Code', 'B001', 'Robert Martin', 'Available', 'N/A')
        self.repo.delete_book('B001')
        self.assertIsNone(self.repo.get_book('B001'))

    def test_delete_all_books(self):
        self.repo.add_book('Clean Code', 'B001', 'Robert Martin', 'Available', 'N/A')
        self.repo.add_book('Refactoring', 'B002', 'Martin Fowler', 'Available', 'N/A')
        self.repo.delete_all_books()
        self.assertEqual(self.repo.get_all_books(), [])


if __name__ == '__main__':
    unittest.main()
