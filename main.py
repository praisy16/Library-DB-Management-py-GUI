import tkinter as tk
from tkinter import messagebox
# assuming your database interaction functions are in a file named database.py
import database


class LibraryManagementSystem:

  def __init__(self, root):
    self.root = root
    self.root.title("Library Management System")
    # self.root.configure(bg='white')  # Set the background to white
    self.root.geometry("800x600")
    self.create_main_menu()

  def create_button(self, text, command):
    button_font = ("Arial", 12, "bold")
    button_color = "#3cb371"
    button_hover_color = "#2e8b57"
    button = tk.Button(self.root,
                       text=text,
                       command=command,
                       font=button_font,
                       bg=button_color,
                       padx=20,
                       pady=10,
                       activebackground=button_hover_color)
    button.bind("<Enter>",
                lambda e, b=button: b.configure(bg=button_hover_color))
    button.bind("<Leave>", lambda e, b=button: b.configure(bg=button_color))
    return button

  def create_main_menu(self):
    self.clear_view()
    self.create_button("Check Out Book",
                       self.setup_checkout_book_view).pack(pady=10)
    self.create_button("Add New Borrower",
                       self.setup_add_borrower_view).pack(pady=10)
    self.create_button("Add New Book", self.setup_add_book_view).pack(pady=10)
    self.create_button("List Copies Loaned Out",
                       self.setup_list_copies_loaned_out_view).pack(pady=10)
    self.create_button("List Late Book Loans",
                       self.setup_list_late_loans_view).pack(pady=10)
    self.create_button("List Borrowers with Late Fee Balances",
                       self.setup_list_borrowers_with_fees_view).pack(pady=10)
    self.create_button("List Book Information with Late Fees",
                       self.setup_list_books_with_fees_view).pack(pady=10)

  def setup_list_late_loans_view(self):
    self.clear_view()

    # Start Date Entry
    tk.Label(self.root, text="Start Due Date (YYYY-MM-DD):").pack(pady=(10, 0))
    self.start_date_entry = tk.Entry(self.root)
    self.start_date_entry.pack(pady=5)

    # End Date Entry
    tk.Label(self.root, text="End Due Date (YYYY-MM-DD):").pack(pady=5)
    self.end_date_entry = tk.Entry(self.root)
    self.end_date_entry.pack(pady=5)

    # Submit Button
    self.create_button("Fetch Late Loans", self.list_late_loans).pack(pady=10)

    # Back to Main Menu Button
    self.create_button("Back to Main Menu",
                       self.create_main_menu).pack(pady=10)

    # Placeholder for results
    self.results_label = tk.Label(self.root)
    self.results_label.pack(pady=10)

  def setup_list_borrowers_with_fees_view(self):
    self.clear_view()

    # Borrower ID Entry
    tk.Label(self.root, text="Borrower ID:").pack(pady=(10, 0))
    self.borrower_id_entry = tk.Entry(self.root)
    self.borrower_id_entry.pack(pady=5)

    # Borrower Name Entry
    tk.Label(self.root, text="Borrower Name:").pack(pady=5)
    self.borrower_name_entry = tk.Entry(self.root)
    self.borrower_name_entry.pack(pady=5)

    # Submit Button
    self.create_button("Search Borrowers",
                       self.search_borrowers_with_fees).pack(pady=10)

    # Back to Main Menu Button
    self.create_button("Back to Main Menu",
                       self.create_main_menu).pack(pady=10)

    # Placeholder for results
    self.borrower_fees_results_label = tk.Label(self.root)
    self.borrower_fees_results_label.pack(pady=10)

  def setup_list_books_with_fees_view(self):
    self.clear_view()

    # Borrower ID Entry
    tk.Label(self.root, text="Borrower ID:").pack(pady=(10, 0))
    self.book_borrower_id_entry = tk.Entry(self.root)
    self.book_borrower_id_entry.pack(pady=5)

    # Book ID Entry
    tk.Label(self.root, text="Book ID:").pack(pady=5)
    self.book_id_entry = tk.Entry(self.root)
    self.book_id_entry.pack(pady=5)

    # Book Title Entry
    tk.Label(self.root, text="Book Title:").pack(pady=5)
    self.book_title_entry = tk.Entry(self.root)
    self.book_title_entry.pack(pady=5)

    # Submit Button
    self.create_button("Search Books",
                       self.search_books_with_fees).pack(pady=10)

    # Back to Main Menu Button
    self.create_button("Back to Main Menu",
                       self.create_main_menu).pack(pady=10)

    # Placeholder for results
    self.books_fees_results_label = tk.Label(self.root)
    self.books_fees_results_label.pack(pady=10)

  def setup_checkout_book_view(self):
    self.clear_view()
    tk.Label(self.root, text="Book ID:").pack(pady=(10, 0))
    self.book_id_entry = tk.Entry(self.root)
    self.book_id_entry.pack(pady=5)
    tk.Label(self.root, text="Branch ID:").pack(pady=5)
    self.branch_id_entry = tk.Entry(self.root)
    self.branch_id_entry.pack(pady=5)
    tk.Label(self.root, text="Card No:").pack(pady=5)
    self.card_no_entry = tk.Entry(self.root)
    self.card_no_entry.pack(pady=5)
    self.create_button("Submit", self.check_out_book).pack(pady=10)
    self.create_button("Back to Main Menu",
                       self.create_main_menu).pack(pady=10)

  def setup_add_borrower_view(self):
    self.clear_view()

    # Add Borrower form elements
    tk.Label(self.root, text="Name:").pack(pady=(10, 0))
    self.borrower_name_entry = tk.Entry(self.root)
    self.borrower_name_entry.pack(pady=5)

    tk.Label(self.root, text="Address:").pack(pady=5)
    self.borrower_address_entry = tk.Entry(self.root)
    self.borrower_address_entry.pack(pady=5)

    tk.Label(self.root, text="Phone:").pack(pady=5)
    self.borrower_phone_entry = tk.Entry(self.root)
    self.borrower_phone_entry.pack(pady=5)

    # Submit and Back buttons
    self.create_button("Submit", self.add_borrower).pack(pady=10)
    self.create_button("Back to Main Menu",
                       self.create_main_menu).pack(pady=10)

  def list_late_loans(self):
    # Retrieve start and end dates from entry fields
    start_date = self.start_date_entry.get()
    end_date = self.end_date_entry.get()

    # Basic validation of date inputs
    if not start_date or not end_date:
      messagebox.showerror("Error", "Both start and end dates are required.")
      return

    try:
      # Assuming there's a function in database.py that fetches late loans
      # For example: database.get_late_loans(start_date, end_date)
      late_loans = database.list_late_returns(start_date, end_date)
      # print(late_loans)
      # Format and display the results
      if late_loans:
        result_text = "\n".join(
          [f"Book ID: {loan[0]}, Days Late: {loan[5]}" for loan in late_loans])
      else:
        result_text = "No late loans found in the given date range."

      self.results_label.config(text=result_text)

    except Exception as e:
      messagebox.showerror("Error", str(e))

  def search_books_with_fees(self):
    borrower_id = self.book_borrower_id_entry.get()
    book_id = self.book_id_entry.get()
    title = self.book_title_entry.get()

    # Validate that at least one field is filled
    if not (borrower_id or book_id or title):
      messagebox.showinfo("Info",
                          "Please enter at least one search criterion.")
      return

    # Call the database function to fetch books with fees based on the criteria
    try:
      # Assuming database.get_books_with_fees() fetches the required information
      books = database.list_books_with_fees(borrower_id, book_id, title)
      print(books)
      # Format and display the results
      if books:
        result_text = "\n".join([
          f"Book ID: {book[0]}, Title: {book[1]}, Fee: {book[2]}"
          for book in books
        ])
      else:
        result_text = "No matching books found."

      self.books_fees_results_label.config(text=result_text)

    except Exception as e:
      messagebox.showerror("Error", str(e))

  def search_borrowers_with_fees(self):
    borrower_id = self.borrower_id_entry.get()
    borrower_name = self.borrower_name_entry.get()

    # Call the database function to fetch borrowers with fees
    try:
      # Assuming database.get_borrowers_with_fees() fetches the required information
      borrowers = database.list_borrowers_with_fees(borrower_id, borrower_name)
      print(borrowers)
      # Format and display the results
      if borrowers:
        result_text = "\n".join([
          f"Borrower ID: {borrower[0]}, Name: {borrower[1]}, Fee Balance: {borrower[2]}"
          for borrower in borrowers
        ])
      else:
        result_text = "No matching borrowers found."

      self.borrower_fees_results_label.config(text=result_text)

    except Exception as e:
      messagebox.showerror("Error", str(e))

  def add_borrower(self):
    # Get values from entry fields
    name = self.borrower_name_entry.get()
    address = self.borrower_address_entry.get()
    phone = self.borrower_phone_entry.get()

    # Validate inputs
    if not name or not address or not phone:
      messagebox.showerror(
        "Error", "Please enter valid values for Name, Address, and Phone.")
      return

    # Call the database function to check out the book
    try:
      result = database.add_borrower(name, address, phone)
      print(result)
      messagebox.showinfo("Success", "New Borrower added.")
      # Display any additional result if necessary
    except Exception as e:
      print(e)
      messagebox.showerror("Error", str(e))

  def setup_add_book_view(self):
    self.clear_view()

    # Add Book form elements
    tk.Label(self.root, text="Book Title:").pack(pady=(10, 0))
    self.book_title_entry = tk.Entry(self.root)
    self.book_title_entry.pack(pady=5)

    tk.Label(self.root, text="Publisher Name:").pack(pady=5)
    self.publisher_name_entry = tk.Entry(self.root)
    self.publisher_name_entry.pack(pady=5)

    tk.Label(self.root, text="Author(s):").pack(pady=5)
    self.author_entry = tk.Entry(self.root)
    self.author_entry.pack(pady=5)

    # Submit and Back buttons
    self.create_button("Submit", self.add_book).pack(pady=10)
    self.create_button("Back to Main Menu",
                       self.create_main_menu).pack(pady=10)

  def setup_list_copies_loaned_out_view(self):
    self.clear_view()

    # Setting up the view to list copies loaned out
    tk.Label(self.root, text="Book Title:").pack(pady=(10, 0))
    self.book_title_search_entry = tk.Entry(self.root)
    self.book_title_search_entry.pack(pady=5)

    # Submit Button
    self.create_button("Search", self.list_copies_loaned_out).pack(pady=10)

    # Back Button
    self.create_button("Back to Main Menu",
                       self.create_main_menu).pack(pady=10)

    # Area to display results
    self.results_label = tk.Label(self.root)
    self.results_label.pack(pady=10)

  def list_copies_loaned_out(self):
    # Retrieve book title from entry field
    book_title = self.book_title_search_entry.get()

    # Validate input
    if not book_title:
      messagebox.showerror("Error", "Please enter a book title.")
      return

    # Call database function to get the number of copies loaned out
    # For example: result = database.get_copies_loaned_out(book_title)
    # Update the results_label with the information
    try:
      # Assuming the function get_copies_loaned_out returns the required information
      result = database.list_copies_loaned_out(book_title)
      self.results_label.config(text=result)
    except Exception as e:
      messagebox.showerror("Error", str(e))

  def check_out_book(self):
    # Get values from entry fields
    book_id = self.book_id_entry.get()
    branch_id = self.branch_id_entry.get()
    card_no = self.card_no_entry.get()

    # Validate inputs
    if not book_id or not branch_id or not card_no:
      messagebox.showwarning("Warning", "All fields are required")
      return

    # Call the database function to check out the book
    try:
      result = database.check_out_book(book_id, branch_id, card_no)
      print(result)
      messagebox.showinfo("Success", "Book checked out successfully")
      # Display any additional result if necessary
    except Exception as e:
      messagebox.showerror("Error", str(e))

  def add_book(self):
    # Retrieve values from entry fields
    title = self.book_title_entry.get()
    publisher = self.publisher_name_entry.get()
    author = self.author_entry.get()
    author = author.split(",")

    # Validate inputs
    if not title or not publisher or not author:
      messagebox.showerror("Error", "All fields are required.")
      return

    try:
      # Assuming the function add_new_book returns a success message
      result = database.add_new_book(title, publisher, author)
      messagebox.showinfo("Success", "New Book added")
    except Exception as e:
      messagebox.showerror("Error", str(e))

  def clear_view(self):
    for widget in self.root.winfo_children():
      widget.destroy()


def main():
  root = tk.Tk()
  app = LibraryManagementSystem(root)
  root.mainloop()


if __name__ == "__main__":
  main()
