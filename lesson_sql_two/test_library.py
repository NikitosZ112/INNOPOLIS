import unittest
from models import LibraryDB, Book, Reader, BorrowedBook


class TestLibraryDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a test database
        cls.db = LibraryDB('library_test', 'postgres', 'password')
        cls.db.engine.execute('DROP SCHEMA IF EXISTS library CASCADE')
        cls.db.create_tables()

    def setUp(self):
        self.session = self.db.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_add_book(self):
        result = self.db.add_book("Test Book", "Test Author", 2023, 5)
        self.assertTrue(result)

        book = self.session.query(Book).filter_by(title="Test Book").first()
        self.assertIsNotNone(book)
        self.assertEqual(book.quantity, 5)

    def test_register_reader(self):
        result = self.db.register_reader("Test Reader", "test@example.com")
        self.assertTrue(result)

        reader = self.session.query(Reader).filter_by(email="test@example.com").first()
        self.assertIsNotNone(reader)

    def test_borrow_return_book(self):
        # Setup
        self.db.add_book("Borrow Test", "Author", 2023, 3)
        self.db.register_reader("Borrower", "borrower@example.com")

        # Borrow
        result = self.db.borrow_book(1, 1)
        self.assertTrue(result)

        book = self.session.query(Book).get(1)
        self.assertEqual(book.quantity, 2)

        # Return
        borrowed = self.session.query(BorrowedBook).filter_by(book_id=1).first()
        result = self.db.return_book(borrowed.id)
        self.assertTrue(result)

        book = self.session.query(Book).get(1)
        self.assertEqual(book.quantity, 3)

    def test_delete_book(self):
        self.db.add_book("Delete Test", "Author", 2023, 1)
        result = self.db.delete_book(2)
        self.assertTrue(result)

        book = self.session.query(Book).get(2)
        self.assertIsNone(book)

    @classmethod
    def tearDownClass(cls):
        # Clean up
        cls.db.engine.execute('DROP SCHEMA IF EXISTS library CASCADE')


if __name__ == '__main__':
    unittest.main()