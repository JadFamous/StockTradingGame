import sqlite3
import os
import re

from database_handler import check_db_and_create, db_path
from portfolio_handler import add_user, edit_user
 
        
def main():
    check_db_and_create()
    while True:
        command = input("Enter command (ADDUSER, EDITUSER, or EXIT to quit): ").upper()
        if command == "EDITUSER":
            edit_user()
        # Handle other commands as before
        if command == "ADDUSER":
            add_user()
        elif command == "EXIT":
            print("Exiting STG Server.")
            break

if __name__ == "__main__":
    main()