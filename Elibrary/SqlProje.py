
import sqlite3

# Veritabanı ile ilgili fonksiyonlar
def create_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_book(title, author, genre, price):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (title, author, genre, price)
        VALUES (?, ?, ?, ?)
    ''', (title, author, genre, price))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM books WHERE id = ?
    ''', (book_id,))
    conn.commit()
    conn.close()

def search_books(query):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ?
    ''', ('%' + query + '%', '%' + query + '%'))
    books = cursor.fetchall()
    conn.close()
    return books

def view_all_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return books

def calculate_total_price(book_ids):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT price FROM books
        WHERE id IN ({})
    '''.format(','.join('?' for _ in book_ids)), book_ids)
    prices = cursor.fetchall()
    total_price = sum(price[0] for price in prices)
    conn.close()
    return total_price

def update_book(book_id, title, author, genre, price):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE books
        SET title = ?, author = ?, genre = ?, price = ?
        WHERE id = ?
    ''', (title, author, genre, price, book_id))
    conn.commit()
    conn.close()
def add_sample_books():
      sample_books = [
            ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 18.99),
            ('1984', 'George Orwell', 'Dystopian', 15.99),
            ('Moby Dick', 'Herman Melville', 'Fiction', 22.50),
            ('The Great Gatsby', 'F. Scott Fitzgerald', 'Classics', 10.99),
            ('War and Peace', 'Leo Tolstoy', 'Historical Fiction', 25.00),
            ('Pride and Prejudice', 'Jane Austen', 'Romance', 12.99),
            ('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 14.99),
            ('Crime and Punishment', 'Fyodor Dostoevsky', 'Psychological Fiction', 19.99),
            ('The Odyssey', 'Homer', 'Epic Poetry', 21.00),
            ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 17.99),
            ('Anna Karenina', 'Leo Tolstoy', 'Drama', 16.50),
            ('Brave New World', 'Aldous Huxley', 'Dystopian', 18.99),
            ('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 14.99),
            ('The Scarlet Letter', 'Nathaniel Hawthorne', 'Classics', 11.99),
            ('Frankenstein', 'Mary Shelley', 'Horror', 13.99),
            ('Dracula', 'Bram Stoker', 'Horror', 17.49),
            ('The Picture of Dorian Gray', 'Oscar Wilde', 'Philosophical Fiction', 20.00),
            ('Fahrenheit 451', 'Ray Bradbury', 'Dystopian', 15.49),
            ('The Road', 'Cormac McCarthy', 'Post-apocalyptic', 19.00),
            ('The Alchemist', 'Paulo Coelho', 'Adventure', 16.99),
            ('Catch-22', 'Joseph Heller', 'Satire', 17.50),
            ('Don Quixote', 'Miguel de Cervantes', 'Classics', 24.99),
            ('Les Misérables', 'Victor Hugo', 'Historical Fiction', 26.00),
            ('The Divine Comedy', 'Dante Alighieri', 'Epic Poetry', 22.00),
            ('The Brothers Karamazov', 'Fyodor Dostoevsky', 'Philosophical Fiction', 23.00),
            ('The Iliad', 'Homer', 'Epic Poetry', 19.50),
            ('The Grapes of Wrath', 'John Steinbeck', 'Fiction', 17.99),
            ('One Hundred Years of Solitude', 'Gabriel García Márquez', 'Magical Realism', 18.50),
            ('Siddhartha', 'Hermann Hesse', 'Philosophical Fiction', 14.50),
            ('The Bell Jar', 'Sylvia Plath', 'Fiction', 15.00),
            ('Slaughterhouse-Five', 'Kurt Vonnegut', 'Science Fiction', 16.99),
            ('The Sun Also Rises', 'Ernest Hemingway', 'Fiction', 17.99),
            ('A Tale of Two Cities', 'Charles Dickens', 'Historical Fiction', 12.99),
            ('Wuthering Heights', 'Emily Brontë', 'Romance', 16.00),
            ('The Secret Garden', 'Frances Hodgson Burnett', 'Children\'s Literature', 10.50),
            ('The Jungle', 'Upton Sinclair', 'Social Fiction', 18.00),
            ('A Clockwork Orange', 'Anthony Burgess', 'Dystopian', 16.99),
            ('The Color Purple', 'Alice Walker', 'Fiction', 14.00),
            ('The Handmaid\'s Tale', 'Margaret Atwood', 'Dystopian', 15.50),
            ('A Wrinkle in Time', 'Madeleine L\'Engle', 'Science Fiction', 11.99),
            ('The Outsiders', 'S.E. Hinton', 'Young Adult', 10.99),
            ('The Fault in Our Stars', 'John Green', 'Young Adult', 13.00),
            ('The Chronicles of Narnia', 'C.S. Lewis', 'Fantasy', 16.00),
            ('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 22.99),
            ('The Hunger Games', 'Suzanne Collins', 'Dystopian', 14.50),
            ('Divergent', 'Veronica Roth', 'Dystopian', 12.99),
            ('The Maze Runner', 'James Dashner', 'Dystopian', 13.50),
            ('The Giver', 'Lois Lowry', 'Dystopian', 11.99),
            ('Twilight', 'Stephenie Meyer', 'Romance', 15.00),
            ('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'Fantasy', 19.99),
            ('The Lord of the Flies', 'William Golding', 'Psychological Fiction', 16.50),
            ('The Shining', 'Stephen King', 'Horror', 21.50),
            ('It', 'Stephen King', 'Horror', 29.00),
            ('The Dark Tower', 'Stephen King', 'Fantasy', 26.99),
            ('The Godfather', 'Mario Puzo', 'Crime', 18.00),
            ('Gone with the Wind', 'Margaret Mitchell', 'Historical Fiction', 20.00),
            ('Sherlock Holmes', 'Arthur Conan Doyle', 'Detective Fiction', 12.99),
            ('The Da Vinci Code', 'Dan Brown', 'Thriller', 14.99),
            ('The Girl with the Dragon Tattoo', 'Stieg Larsson', 'Thriller', 16.99),
            ('Murder on the Orient Express', 'Agatha Christie', 'Crime', 13.99),
            ('And Then There Were None', 'Agatha Christie', 'Crime', 14.50),
            ('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 15.99),
            ('The Help', 'Kathryn Stockett', 'Historical Fiction', 18.00),
            ('The Book Thief', 'Markus Zusak', 'Historical Fiction', 16.50),
            ('The Night Circus', 'Erin Morgenstern', 'Fantasy', 20.00),
            ('The Shadow of the Wind', 'Carlos Ruiz Zafón', 'Mystery', 17.00),
            ('The Paris Library', 'Janet Skeslien Charles', 'Historical Fiction', 18.50),
            ('The Tattooist of Auschwitz', 'Heather Morris', 'Historical Fiction', 16.00),
            ('Educated', 'Tara Westover', 'Memoir', 15.99),
            ('Becoming', 'Michelle Obama', 'Memoir', 17.50),
            ('The Glass Castle', 'Jeannette Walls', 'Memoir', 14.00),
            ('Where the Crawdads Sing', 'Delia Owens', 'Mystery', 19.00),
            ('Little Women', 'Louisa May Alcott', 'Classics', 12.00),
            ('Emma', 'Jane Austen', 'Romance', 13.99),
            ('Sense and Sensibility', 'Jane Austen', 'Romance', 14.99),
            ('North and South', 'Elizabeth Gaskell', 'Romance', 16.00),
            ('Jane Eyre', 'Charlotte Brontë', 'Romance', 17.00),
            ('The Little Prince', 'Antoine de Saint-Exupéry', 'Children\'s Literature', 9.99),
            ('The Velveteen Rabbit', 'Margery Williams', 'Children\'s Literature', 8.99),
            ('Charlotte\'s Web', 'E.B. White', 'Children\'s Literature', 10.99),
            ('Matilda', 'Roald Dahl', 'Children\'s Literature', 12.99),
            ('Alice\'s Adventures in Wonderland', 'Lewis Carroll', 'Children\'s Literature', 7.99),
            ('The Wind in the Willows', 'Kenneth Grahame', 'Children\'s Literature', 9.50),
            ('The Tale of Peter Rabbit', 'Beatrix Potter', 'Children\'s Literature', 5.99),
            ('The Adventures of Tom Sawyer', 'Mark Twain', 'Classics', 10.00),
            ('Treasure Island', 'Robert Louis Stevenson', 'Adventure', 12.00),
            ('Robinson Crusoe', 'Daniel Defoe', 'Adventure', 14.50),
            ('Around the World in 80 Days', 'Jules Verne', 'Adventure', 15.00),
            ('Journey to the Center of the Earth', 'Jules Verne', 'Science Fiction', 13.99),
            ('20,000 Leagues Under the Sea', 'Jules Verne', 'Adventure', 14.00),
            ('The Call of the Wild', 'Jack London', 'Adventure', 12.50),
            ('White Fang', 'Jack London', 'Adventure', 13.00),
            ('The Last of the Mohicans', 'James Fenimore Cooper', 'Historical Fiction', 15.00),
            ('The Three Musketeers', 'Alexandre Dumas', 'Adventure', 16.00),
            ('Les Misérables', 'Victor Hugo', 'Historical Fiction', 17.99),
            ('The Count of Monte Cristo', 'Alexandre Dumas', 'Adventure', 18.50),
            ('The Hunchback of Notre-Dame', 'Victor Hugo', 'Historical Fiction', 15.99)
      ]

      for book in sample_books:
        add_book(book[0], book[1], book[2], book[3])

