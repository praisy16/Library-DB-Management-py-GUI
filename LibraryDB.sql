CREATE TABLE PUBLISHER (
  Publisher_Name VARCHAR(200) PRIMARY KEY,
  Phone INTEGER(10),
  Address VARCHAR(200)
);


CREATE TABLE LIBRARY_BRANCH (
  Branch_Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Branch_Name VARCHAR(200),
  Branch_Address VARCHAR(255)
);


CREATE TABLE BORROWER (
  Card_No INTEGER PRIMARY KEY AUTOINCREMENT,
  Name VARCHAR(200),
  Address VARCHAR(200),
  Phone INTEGER(10)
);


CREATE TABLE BOOK (
  Book_Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Title VARCHAR(200),
  Publisher_Name VARCHAR(200),
  FOREIGN KEY (Publisher_Name) REFERENCES PUBLISHER(Publisher_Name)
);



CREATE TABLE BOOK_LOANS (
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
);


CREATE TABLE BOOK_COPIES(
  Book_Id INTEGER,
  Branch_Id INTEGER,
  No_Of_Copies INTEGER,
  PRIMARY KEY(Book_Id, Branch_Id),
  FOREIGN KEY (Book_Id) REFERENCES BOOK(Book_Id),
  FOREIGN KEY (Branch_Id) REFERENCES LIBRARY_BRANCH(Branch_Id)
);


CREATE TABLE BOOK_AUTHORS(
  Book_Id INTEGER,
  Author_Name VARCHAR(200),
  PRIMARY KEY(Book_Id, Author_Name),
  FOREIGN KEY (Book_Id) REFERENCES BOOK(Book_Id)
);


--load data 
.mode csv
.import Book.csv BOOK
.import Book_Authors.csv BOOK_AUTHORS
.import Book_Copies.csv BOOK_COPIES
.import Book_Loans.csv BOOK_LOANS
.import Library_Branch.csv LIBRARY_BRANCH
.import Publisher.csv PUBLISHER
.import Borrower.csv BORROWER


-- adding project pt 2 updates

  INSERT INTO BORROWER (Name, Address,Phone)
    VALUES ('Aindrila', 'Arlington', '673-929-0190');

  UPDATE BORROWER
  SET PHONE = '837-721-8965'
  WHERE Name = 'XYZ';

  UPDATE BOOK_COPIES
  SET No_Of_Copies = No_Of_Copies + 1
  WHERE Branch_Id = 3;

  INSERT INTO BOOK(Title, Publisher_Name)
  VALUES ('XYZ', 'Oxford Publishing');

  INSERT INTO BOOK_AUTHORS(Book_Id, Author_Name)
  VALUES ('22', 'JK Rowling');

  INSERT INTO LIBRARY_BRANCH(Branch_Name, Branch_Address)
  VALUES ('North Branch', '456 NW, Irving, TX 76100');

  INSERT INTO LIBRARY_BRANCH(Branch_Name, Branch_Address)
  VALUES ('UTA Branch', '123 Cooper St, Arlington, TX 76101');

-- adding late
  ALTER TABLE Book_Loans ADD COLUMN Late INTEGER;

UPDATE Book_Loans
SET Late = (CASE
  WHEN Returned_Date != 'NULL' AND Returned_Date > Due_Date THEN 1
  WHEN Returned_Date IS NOT NULL AND Returned_Date <= Due_Date THEN 0
  ELSE NULL

  END);

--query 2

ALTER TABLE Library_Branch ADD COLUMN LateFee INTEGER;

UPDATE Library_Branch
SET LateFee = (CASE
  WHEN Branch_Id = 1 THEN 20
  ELSE 10

  END);

--query 3

CREATE VIEW vBookLoanInfo AS  
  SELECT BL.Card_No,
  B.Name,
  BL.Date_Out,
  Bl.Due_Date, 
  BL.Returned_Date, (CASE
            WHEN Returned_Date != 'NULL' THEN (julianday(BL.Returned_Date) - julianday(BL.Date_Out))
            ELSE NULL
            END) AS 'TotalDays', Book.Title, (CASE
            WHEN Returned_Date != 'NULL' AND Returned_Date > Due_Date THEN (julianday(BL.Returned_Date) - julianday(BL.Due_Date))
            ELSE 0
            END) AS 'Number of days returned late', BL.Branch_Id, (CASE
            WHEN Returned_Date != 'NULL' AND Returned_Date > Due_Date THEN (CASE WHEN Branch_Id = 1 THEN 20 ELSE 10 END)
            ELSE 0
            END) AS 'LateFee'
    FROM Book_Loans BL, Borrower B, Book
    WHERE BL.Card_No = B.Card_No AND Book.Book_Id = BL.Book_Id;

--book_loans trigger
CREATE TRIGGER validate_book_loan
AFTER INSERT ON BOOK_LOANS
FOR EACH ROW
BEGIN
UPDATE BOOK_COPIES
SET No_Of_Copies = No_Of_Copies-1
WHERE Book_Id = NEW.BOOK_ID and branch_id = NEW.branch_id;
END;


