import sqlite3
import os

# Database path
db_path = 'D:\\Projects\\STG\\PORTFOLIO.db'

def check_db_and_create():
    """Check for the existence of the PORTFOLIO.db and create it with the initial table if not exists."""
    table_creation_query = """
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
    db_exists = os.path.exists(db_path)
    with sqlite3.connect(db_path) as conn:
        if not db_exists:
            conn.execute(table_creation_query)
            print("Database and table created successfully.")
        else:
            print("Database found. Ready for operations.")