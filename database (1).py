import sqlite3
from pprint import pprint


def connect_to_database():
  """Connect to the SQLite database and return the connection and cursor."""
  connection = sqlite3.connect("library.db")
  cursor = connection.cursor()
  return connection, cursor


def close_connection(connection):
  """Close the database connection."""
  if connection:
    connection.close()


def create_publisher_table(cursor):
  # create publisher table
  cursor.execute('''CREATE TABLE IF NOT EXISTS PUBLISHER (
      Publisher_Name VARCHAR(200) PRIMARY KEY,
      Phone INTEGER(10),
      Address VARCHAR(200)
  )''')


def create_book_table(cursor):
  # create book table
  cursor.execute('''CREATE TABLE IF NOT EXISTS BOOK (
      Book_Id INTEGER PRIMARY KEY,
      Title VARCHAR(200),
      Publisher_Name VARCHAR(200),
      FOREIGN KEY (Publisher_Name) REFERENCES PUBLISHER(Publisher_Name)
  )''')


def create_library_branch_table(cursor):
  # create branch table
  cursor.execute('''CREATE TABLE IF NOT EXISTS LIBRARY_BRANCH (
      Branch_Id INTEGER PRIMARY KEY AUTOINCREMENT,
      Branch_Name VARCHAR(200),
      Branch_Address VARCHAR(255)
  )''')


def create_borrower_table(cursor):
  # create borrower table
  cursor.execute('''CREATE TABLE IF NOT EXISTS BORROWER (
      Card_No INTEGER PRIMARY KEY AUTOINCREMENT,
      Name VARCHAR(200),
      Address VARCHAR(200),
      Phone INTEGER(10)
  )''')


def create_book_loans_table(cursor):
  # create book_loans table
  cursor.execute('''CREATE TABLE IF NOT EXISTS BOOK_LOANS (
      Book_Id INTEGER,
      Branch_Id INTEGER,
      Card_No INTEGER,
      Date_Out DATE,
      Due_Date DATE,
      Returned_Date DATE,
      PRIMARY KEY (Book_Id, Branch_Id, Card_No),
      FOREIGN KEY (Book_Id) REFERENCES BOOK(Book_Id),
      FOREIGN KEY (Branch_Id) REFERENCES LIBRARY_BRANCH(Branch_Id),
      FOREIGN KEY (Card_No) REFERENCES BORROWER(Card_No)
  )''')


def create_book_authors(cursor):
  cursor.execute('''
        CREATE TABLE IF NOT EXISTS BOOK_AUTHORS(
            Book_Id INTEGER,
            Author_Name VARCHAR(200),
            PRIMARY KEY(Book_Id, Author_Name),
            FOREIGN KEY(Book_Id) REFERENCES BOOK(Book_Id)
    )''')


def execute_query_2(query, params=()):
  """Execute a given SQL query with optional parameters and return the result."""
  conn, cursor = connect_to_database()
  cursor.execute(query, params)
  results = cursor.fetchall()
  conn.commit()
  close_connection(conn)
  return results


#def execute_query(cursor, query, params=()):
  # execute some query
 # cursor.execute(query, params)
  #rows = cursor.fetchall()
  #for row in rows:
  #  print(row)
  #return rows


def check_out_book(book_id, branch_id, card_no):
  """Function to handle checking out a book."""
  try:
    checkout_query = '''INSERT INTO Book_Loans (Book_Id, Branch_Id, Card_No, Date_Out, Due_Date) 
                            VALUES (?, ?, ?, CURRENT_DATE, DATE('now', '+14 days'))'''
    execute_query_2(checkout_query, (book_id, branch_id, card_no))

    # Assuming a trigger automatically updates the Book_Copies table.
    # Fetch and return the updated Book_Copies for confirmation.
    fetch_query = '''SELECT * FROM Book_Copies WHERE Book_Id = ? AND Branch_Id = ?'''
    return execute_query_2(fetch_query, (book_id, branch_id))
  except Exception as e:
    print(f"ERROR in check out book: {e}")
    return e


def add_borrower(name, address, phone):
  """Function to add a new borrower and return the new CardNo."""
  add_borrower_query = '''INSERT INTO Borrower (Name, Address, Phone) VALUES (?, ?, ?)'''
  execute_query_2(add_borrower_query, (name, address, phone))

  get_card_no_query = '''SELECT last_insert_rowid()'''
  return execute_query_2(get_card_no_query)


def add_new_book(title, publisher_name, authors):
  """Function to add a new book and its copies to all branches."""
  # Add new book
  add_book_query = '''INSERT INTO Book (Title, Publisher_Name) VALUES (?, ?)'''
  execute_query_2(add_book_query, (title, publisher_name))

  # Get the new book id
  book_id_query = '''SELECT Book_Id FROM Book WHERE Title = ?'''
  book_id = execute_query_2(book_id_query, (title, ))[0][0]
  print("Book ID Added: ", book_id)
  # Add authors (assuming a many-to-many relationship with an Authors table)
  for author in authors:
    add_author_query = '''INSERT INTO Book_Authors (Book_Id, Author_Name) VALUES (?, ?)'''

    result = execute_query_2(add_author_query, (book_id, author))
    # pprint(result)
  # Add copies to each branch (assuming 5 branches and 5 copies each)
  for branch_id in range(1, 6):
    add_copies_query = '''INSERT INTO Book_Copies (Book_Id, Branch_Id, No_Of_Copies) VALUES (?, ?, 5)'''
    execute_query_2(add_copies_query, (book_id, branch_id))


def list_copies_loaned_out(book_title):
  """Function to list the number of copies loaned out per branch for a given book title."""
  query = '''
      SELECT lb.Branch_Name, COUNT(*) as Loaned_Out_Copies
      FROM Book_Loans bl
      JOIN BOOK b ON bl.Book_Id = b.Book_Id
      JOIN LIBRARY_BRANCH lb ON bl.Branch_Id = lb.Branch_Id
      WHERE b.Title = ?
      GROUP BY lb.Branch_Name
  '''
  return execute_query_2(query, (book_title, ))


def validate_book_loan_trigger():
  query = """CREATE TRIGGER IF NOT EXISTS VALIDATE_BOOK_LOAN
    AFTER INSERT ON BOOK_LOANS
    BEGIN
    UPDATE BOOK_COPIES
    SET No_Of_Copies = No_Of_Copies+1
    WHERE BOOK_LOANS.Book_Id = Book_Copies.BOOK_ID and book_loans.branch_id = book_copies.branch_id;
    END;"""
  return execute_query_2(query)


def list_late_returns(start_due_date, end_due_date):
  query = """
    SELECT Book_Id, Branch_Id, Card_No, Due_Date, Returned_Date, 
           JULIANDAY(Returned_Date) - JULIANDAY(Due_Date) AS Days_Late
    FROM Book_Loans
    WHERE Returned_Date > Due_Date
      AND Due_Date BETWEEN ? AND ?
    ORDER BY Days_Late DESC;
    """
  try:
    results = execute_query_2(query, (start_due_date, end_due_date))
    return results
  except sqlite3.Error as e:
    raise Exception(f"Database error: {e}")


def list_borrowers_with_fees(filter_id=None, filter_name=None):
  query = """
    SELECT 
        br.Card_No AS Borrower_ID, 
        br.Name AS Borrower_Name, 
        COALESCE('$' || CAST(SUM(lb.LateFee) AS DECIMAL(10, 2)), '$0.00') AS LateFee_Balance
    FROM 
        Borrower br
    LEFT JOIN 
        Book_Loans bl ON br.Card_No = bl.Card_No
    LEFT JOIN 
        Library_Branch lb ON bl.Branch_Id = lb.Branch_Id
    WHERE 
        (? IS NULL OR br.Card_No = ?) OR (? IS NULL OR br.Name LIKE ?)
    GROUP BY 
        br.Card_No
    ORDER BY 
        (CASE WHEN ? IS NULL THEN SUM(lb.LateFee) ELSE NULL END) DESC;
    """

  params = (filter_id, filter_id, filter_name,
            f'%{filter_name}%' if filter_name else None, filter_id)
  try:
    results = execute_query_2(query, params)
    return results
  except sqlite3.Error as e:
    raise Exception(f"Database error: {e}")


def list_books_with_fees(filter_borrower_id=None,
                         filter_book_id=None,
                         filter_title=None):

  query = """
    SELECT 
        b.Book_Id AS Book_ID,
        b.Title AS Book_Title,
        COALESCE('$' || CAST(SUM(lb.LateFee) AS DECIMAL(10, 2)), 'Non-Applicable') AS Late_Fee
    FROM 
        Book b
    LEFT JOIN 
        Book_Loans bl ON b.Book_Id = bl.Book_Id
    LEFT JOIN 
        Library_Branch lb ON bl.Branch_Id = lb.Branch_Id
    WHERE 
        (? IS NULL OR bl.Card_No = ?)
        OR (? IS NULL OR b.Book_Id = ?)
        OR (? IS NULL OR b.Title LIKE ?)
    GROUP BY 
        b.Book_Id
    ORDER BY 
        (CASE WHEN ? IS NULL THEN SUM(lb.LateFee) ELSE NULL END) DESC;
    """

  params = (filter_borrower_id, filter_borrower_id, filter_book_id,
            filter_book_id, filter_title,
            f'%{filter_title}%' if filter_title else None, filter_borrower_id)
  try:
    results = execute_query_2(query, params)
    return results
  except sqlite3.Error as e:
    raise Exception(f"Database error: {e}")


# Example usage
if __name__ == "__main__":
  connection, cursor = connect_to_database()

  create_book_table(cursor)
  create_publisher_table(cursor)
  create_library_branch_table(cursor)
  create_borrower_table(cursor)
  create_book_loans_table(cursor)
  create_book_authors(cursor)
  # validate_book_loan_trigger()

  table_name = "Book_Copies"
  test_query = f"""SELECT * from {table_name};"""
  # test_query = f"""PRAGMA table_info({table_name});"""
  # test_query = "SELECT Book_Id FROM Book WHERE Title = 1984"
  pprint(execute_query_2(test_query))
