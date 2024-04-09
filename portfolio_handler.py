import sqlite3
import re
from database_handler import db_path


def add_user():
    """Facilitates the addition of a new user to the Account_Portfolios table, enforcing unique (case-insensitive) usernames."""
    while True:
        username = input("Enter a new username (or type MAINMENU to return): ")
        if username.upper() == "MAINMENU":
            return
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Use LOWER function for case-insensitive comparison
            cursor.execute("SELECT * FROM Account_Portfolios WHERE LOWER(username) = LOWER(?)", (username,))
            if cursor.fetchone():
                print("This username already exists (usernames are case-insensitive). Please enter a different username.")
                continue
            if not 5 <= len(username) <= 32 or not re.match("^[A-Za-z0-9]+$", username):
                print("Username must be 5-32 characters long and consist only of letters A-Z and numbers 0-9.")
                continue
            # Insert the new user into the database with specified initial values and account_type set to novice_trader
            try:
                insert_query = """
                INSERT INTO Account_Portfolios 
                (username, account_type, available_currency, hold_currency, owned_stocks, owned_shares, owned_shares_class)
                VALUES (?, 'novice_trader', ?, ?, ?, ?, ?)
                """
                # Setting specific initial values for the new user
                cursor.execute(insert_query, (username, 5000.00, 0.00, 'BASIC', 1, 'Class_C'))
                conn.commit()
                print("Account has been created with $5000.00 available currency, BASIC stock, 1 share, Class_C, and account type novice_trader.")
                return  # Exit after successful creation
            except sqlite3.Error as e:
                print(f"An error occurred while creating the account: {e}")
                return  # Consider retrying or exiting based on your error handling policy
            
def edit_user():
    """Facilitates the editing of an existing user in the Account_Portfolios table."""
    account_id = input("Enter the account_id of the user you want to edit: ")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Account_Portfolios WHERE account_id = ?", (account_id,))
        user_row = cursor.fetchone()
        if not user_row:
            print("No user found with the provided account_id.")
            return
        
        print("Which value do you want to change?")
        print("1. Username")
        print("2. Account Type")
        print("3. Available Currency")
        print("4. Hold Currency")
        print("5. Owned Stocks")
        print("6. Owned Shares")
        print("7. Owned Shares Class")
        choice = input("Enter the number of your choice: ")

        column = None
        valid_input = False
        new_value = None

        # Determine which column is being edited
        if choice == '1':
            column = 'username'
            while not valid_input:
                new_value = input("Enter the new username: ")
                if 5 <= len(new_value) <= 32 and re.match("^[A-Za-z0-9]+$", new_value):
                    valid_input = True
                else:
                    print("Username must be 5-32 characters long and consist only of letters A-Z and numbers 0-9.")
        
        if choice == '2':
            column = 'account_type'
            while not valid_input:
                new_value = input("Enter the new account type: ")
                if new_value == 'Novice Trader' or new_value == 'Advanced Trader' or new_value == 'Expert Trader' or new_value == 'Developer': 
                    valid_input = True
                else:
                    print("Account type must be Novice Trader, Advanced Trader, Expert Trader, or Developer.")

        if choice == '3':
            column = 'available_currency'
            while not valid_input:
                new_value = float(input("Enter the new available currency: "))
                if new_value >= 0:
                    valid_input = True
                else:
                    print("Available currency must be greater than or equal to 0.") 

        if choice == '4':
            column = 'hold_currency'
            while not valid_input:
                new_value = float(input("Enter the new hold currency: "))
                if new_value >= 0:
                    valid_input = True
                else:
                    print("Hold currency must be greater than or equal to 0.")

        if choice == '5':
            column = 'owned_stocks'
            while not valid_input:
                new_value = input("Enter the new owned stock(s): ")
                if new_value == 'BASIC':
                    valid_input = True
                else:
                    print("Owned stocks must be active stocks.")

        if choice == '6':
            column = 'owned_shares'
            while not valid_input:
                new_value = int(input("Enter the new owned shares: "))
                if new_value >= 0:
                    valid_input = True
                else:
                    print("Owned shares must be greater than or equal to 0.")

        if choice == '7':
            column = 'owned_shares_class'
            while not valid_input:
                new_value = input("Enter the new owned shares class: ")
                if new_value == 'Class_C' or new_value == 'Class_B' or new_value == 'Class_A':
                    valid_input = True
                else:
                    print("Owned shares class must be Class_C, Class_B, or Class_A.")

        if not column:
            print("Invalid selection.")
            return

        # Ask for approval before making the change
        while True:
            approval = input("Type APPROVEEDIT to confirm the change, or MAINMENU to cancel: ").upper()
            if approval == "MAINMENU":
                return  # Cancel the operation
            elif approval == "APPROVEEDIT":
                # Update the database with the new value
                update_query = f"UPDATE Account_Portfolios SET {column} = ? WHERE account_id = ?"
                cursor.execute(update_query, (new_value, account_id))
                conn.commit()
                print(f"{column} has been updated to {new_value}.")
                return
            else:
                print("Please type APPROVEEDIT to confirm or MAINMENU to cancel.")