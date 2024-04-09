import sqlite3
from database_handler import db_paths, setup_portfolio_db, setup_companies_db
from portfolio_handler import add_user, edit_user

# Initialize databases on startup
setup_portfolio_db()
setup_companies_db()

def add_company():
    """Adds a new company ticker symbol to the Current_Tickers table."""
    while True:
        ticker_symbol = input("Enter a Ticker Symbol (1-5 chars, at least 1 letter, A-Z, 0-9): ").upper()
        if not (1 <= len(ticker_symbol) <= 5) or not any(c.isalpha() for c in ticker_symbol) or not ticker_symbol.isalnum():
            print("Invalid ticker symbol. Must be 1-5 characters, include at least one letter, and be alphanumeric.")
            continue
        with sqlite3.connect(db_paths['companies']) as conn:
            try:
                conn.execute("INSERT INTO Current_Tickers (ticker_symbol) VALUES (?)", (ticker_symbol,))
                conn.commit()
                print(f"Ticker symbol {ticker_symbol} added successfully.")
                break
            except sqlite3.IntegrityError:
                print("This ticker symbol already exists. Please try a different one.")

def remove_company():
    """Removes a company ticker symbol from the Current_Tickers table."""
    ticker_symbol = input("Enter the ticker symbol you wish to remove: ").upper()
    with sqlite3.connect(db_paths['companies']) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Current_Tickers WHERE ticker_symbol = ?", (ticker_symbol,))
        if cursor.fetchone():
            approval = input("Type APPROVEREMOVAL to confirm the removal: ").upper()
            if approval == "APPROVEREMOVAL":
                conn.execute("DELETE FROM Current_Tickers WHERE ticker_symbol = ?", (ticker_symbol,))
                conn.commit()
                print(f"Ticker symbol {ticker_symbol} has been removed successfully.")
            else:
                print("Removal not confirmed. No changes were made.")
        else:
            print(f"No ticker symbol found for {ticker_symbol}.")

def main():
    while True:
        command = input("Enter command (ADDUSER, EDITUSER, ADDCOMPANY, REMOVECOMPANY, or EXIT): ").upper()
        if command == "EXIT":
            print("Exiting the program.")
            break
        elif command == "ADDUSER":
            add_user()
        elif command == "EDITUSER":
            edit_user()
        elif command == "ADDCOMPANY":
            add_company()
        elif command == "REMOVECOMPANY":
            remove_company()
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
