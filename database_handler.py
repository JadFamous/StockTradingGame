import sqlite3
import os

db_path_portfolio = 'D:\\Projects\\STG\\PORTFOLIO.db'
db_path_companies = 'D:\\Projects\\STG\\COMPANIES.db'

def check_db_and_create_portfolio():
    """Check and create the PORTFOLIO.db with its initial table if not exists."""
    table_creation_query_portfolio = """
    CREATE TABLE IF NOT EXISTS Account_Portfolios (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE CHECK(length(username) >= 5 AND length(username) <= 32),
        account_type TEXT NOT NULL,
        available_currency REAL NOT NULL CHECK(available_currency >= 0),
        hold_currency REAL NOT NULL CHECK(hold_currency >= 0),
        owned_stocks TEXT CHECK(length(owned_stocks) >= 1 AND length(owned_stocks) <= 5),
        owned_shares INTEGER NOT NULL CHECK(owned_shares >= 0),
        owned_shares_class TEXT NOT NULL
    );
    """
    _check_and_create(db_path_portfolio, table_creation_query_portfolio)

def check_db_and_create_companies():
    """Check and create the COMPANIES.db with its initial table if not exists."""
    table_creation_query_companies = """
    CREATE TABLE IF NOT EXISTS Current_Tickers (
        ticker_symbol TEXT PRIMARY KEY CHECK(length(ticker_symbol) >= 1 AND length(ticker_symbol) <= 5 AND ticker_symbol GLOB '*[A-Z]*')
    );
    """
    _check_and_create(db_path_companies, table_creation_query_companies)

def _check_and_create(db_path, creation_query):
    """Generic function to check if a database exists and create it with the specified table."""
    db_exists = os.path.exists(db_path)
    with sqlite3.connect(db_path) as conn:
        if not db_exists:
            conn.execute(creation_query)
            print(f"Database and table created successfully at {db_path}.")
        else:
            print(f"Database found at {db_path}. Ready for operations.")

# Ensure both database checks are called when this module is imported
check_db_and_create_portfolio()
check_db_and_create_companies()
