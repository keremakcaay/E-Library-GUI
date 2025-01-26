from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt
import sqlite3
import sys
from SqlProje import view_all_books  # Assuming you already have a function to get all books from the database

class ELibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E-Library")
        self.setGeometry(200, 100, 800, 600)

        self.init_ui()
        self.create_database()  # Ensure the database and table are created
        self.load_books()  # Load books from the database on startup

    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Input fields and buttons for book operations
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Book Title")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author")
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Genre")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price")

        add_button = QPushButton("Add Book")
        add_button.clicked.connect(self.add_book)
        
        update_button = QPushButton("Update Book")
        update_button.clicked.connect(self.update_book)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search books by title or author")
        search_input.textChanged.connect(self.search_books)

        calculate_button = QPushButton("Calculate Total Price")
        calculate_button.clicked.connect(self.calculate_total_price)

        # Table for displaying books
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(5)
        self.books_table.setHorizontalHeaderLabels(["ID", "Title", "Author", "Genre", "Price"])
        self.books_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.books_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.books_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        delete_button = QPushButton("Delete Book")
        delete_button.clicked.connect(self.delete_book)

        # Layout for input fields
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.title_input)
        input_layout.addWidget(self.author_input)
        input_layout.addWidget(self.genre_input)
        input_layout.addWidget(self.price_input)
        input_layout.addWidget(add_button)

        # Add widgets to main layout
        main_layout.addLayout(input_layout)
        main_layout.addWidget(update_button)
        main_layout.addWidget(search_input)
        main_layout.addWidget(self.books_table)
        main_layout.addWidget(delete_button)
        main_layout.addWidget(calculate_button)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_database(self):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()

        # Create table with a UNIQUE constraint on title and author
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT,
                price REAL,
                UNIQUE(title, author)
            )
        ''')
        connection.commit()
        connection.close()

        # Add sample books only if the table was created
        self.add_sample_books()

    def execute_query(self, query, parameters=()):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        connection.commit()
        connection.close()

    def is_book_in_database(self, title, author):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        cursor.execute('''
            SELECT 1 FROM books WHERE title = ? AND author = ?
        ''', (title, author))
        result = cursor.fetchone()
        connection.close()
        return result is not None

    def add_sample_books(self):
        sample_books = [
            ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 18.99),
            ('1984', 'George Orwell', 'Dystopian', 15.99),
            ('Moby Dick', 'Herman Melville', 'Fiction', 22.50),
            ('The Great Gatsby', 'F. Scott Fitzgerald', 'Classics', 10.99),
            ('War and Peace', 'Leo Tolstoy', 'Historical Fiction', 25.00),
        ]

        for book in sample_books:
            try:
                self.execute_query('''
                    INSERT INTO books (title, author, genre, price)
                    VALUES (?, ?, ?, ?)
                ''', (book[0], book[1], book[2], book[3]))
            except sqlite3.IntegrityError:
                print(f"Book '{book[0]}' by {book[1]} already exists in the database.")

    def load_books(self):
        books = view_all_books()  # Get all books from the database
        self.books_table.setRowCount(len(books))
        for row_idx, book in enumerate(books):
            for col_idx, value in enumerate(book):
                self.books_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        genre = self.genre_input.text()
        price = self.price_input.text()

        if not title or not author or not genre or not price:
            QMessageBox.warning(self, "Input Error", "All fields must be filled!")
            return

        try:
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Price must be a valid number!")
            return

        self.execute_query("INSERT INTO books (title, author, genre, price) VALUES (?, ?, ?, ?)",
                           (title, author, genre, price))
        self.load_books()
        self.clear_inputs()

    def delete_book(self):
        selected_items = self.books_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "No book selected!")
            return

        book_id = int(selected_items[0].text())
        self.execute_query("DELETE FROM books WHERE id = ?", (book_id,))
        self.load_books()

    def update_book(self):
        selected_items = self.books_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "No book selected!")
            return

        book_id = int(selected_items[0].text())
        title = self.title_input.text()
        author = self.author_input.text()
        genre = self.genre_input.text()
        price = self.price_input.text()

        if not title or not author or not genre or not price:
            QMessageBox.warning(self, "Input Error", "All fields must be filled!")
            return

        try:
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Price must be a valid number!")
            return

        self.execute_query("""
            UPDATE books
            SET title = ?, author = ?, genre = ?, price = ?
            WHERE id = ?
        """, (title, author, genre, price, book_id))
        self.load_books()
        self.clear_inputs()

    def search_books(self, query):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{query}%", f"%{query}%"))
        books = cursor.fetchall()
        connection.close()

        # Remove duplicates from the results
        unique_books = {}
        for book in books:
            key = (book[1], book[2])  # Use (title, author) as the unique key
            if key not in unique_books:
                unique_books[key] = book

        books = list(unique_books.values())

        # Populate the table
        self.books_table.setRowCount(len(books))
        for row_idx, book in enumerate(books):
            for col_idx, value in enumerate(book):
                self.books_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def calculate_total_price(self):
        selected_items = self.books_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "No books selected!")
            return

        selected_rows = set(item.row() for item in selected_items)
        total_price = 0
        for row in selected_rows:
            price_item = self.books_table.item(row, 4)  # Price is in column 4
            total_price += float(price_item.text())

        QMessageBox.information(self, "Total Price", f"Total price of selected books: ${total_price:.2f}")

    def clear_inputs(self):
        self.title_input.clear()
        self.author_input.clear()
        self.genre_input.clear()
        self.price_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ELibraryApp()
    window.show()
    sys.exit(app.exec())
