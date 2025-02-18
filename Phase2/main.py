"""
Main Banking System

Description:
This program simulates a banking system that allows users to perform transactions such as withdrawals, 
transfers, and bill payments. Users must log in before performing transactions. The system supports 
both standard and admin sessions, where the admin has special privileges such as overriding account 
limits and accessing all user accounts.

Input Files:
- None (User accounts are hardcoded into the program) #TODO: current user accounts file, available rental units file

Output Files:
- daily_transaction_file.txt: Stores a record of all transactions performed during a session (Maybe need to break transactions as day by day).

How to Run:
1. Start the program.
2. Enter "login" to authenticate.
   - Admin users enter "admin" to log in with full access.
   - Standard users enter their username to log in.
3. After login, enter one of the following commands:
   - "withdrawal" to withdraw funds from the logged-in account.
   - "transfer" to transfer funds between accounts.
   - "paybill" to pay a bill to a predefined company.
   - "logout" to end the session and save the transactions.
   - TODO: Add rest features
4. Transactions are logged in the output file upon execution.
"""

from transfer import Transfer
from paybill import Paybill
from check import Check
from deposit import Deposit
from create import Create
from changeplan import ChangePlan
from disable import Disable

class User:
    def __init__(self, account_number, user_name, availability, balance):
        self.account_number = account_number
        self.user_name = user_name.strip()
        self.availability = availability  # "A" for active, "D" for disabled
        self.balance = float(balance)
        self.user_type = "standard"  # Default all users to "standard"

#TODO： Hardcoded users, should be read the txt file to get it
USERS = {
    "00001": User("00001", "Dev Thaker", "A", 500.00),
    "00002": User("00002", "Wenbo Zhang", "D", 250.00),
    "00003": User("00003", "Xuan Zheng", "A", 1400.00),
    "00004": User("00004", "Neel Shah", "A", 0.00),
    "00005": User("00005", "Jeremy Bradbury", "D", 1500.00),
    "00006": User("00006", "Riddhi More", "A", 2200.00),
    "00007": User("00007", "Emon Roy", "A", 750.00),
    "00008": User("00008", "Eve Adams", "A", 300.00),
}

# For transaction file
TRANSACTION_FILE = "daily_transaction_file.txt"

def log_transaction(transaction):
    with open(TRANSACTION_FILE, "a") as file:
        file.write(transaction + "\n")

def banking_system():
    logged_in = False
    current_user = None
    session_type = None
    check = Check()
    
    while True:
        command = input("Enter command: ").strip().lower()
        
        if command == "login":
            print("Welcome to the banking system.")
            
            if logged_in:
                print("You are already logged in.")
                continue
            
            session_type = input("Enter session type: ").strip().lower()
            if session_type == "admin":
                logged_in = True
                current_user = None
            else:
                user_name = input("Enter account holder name: ").strip()
                found_user = None
                for user in USERS.values():
                    if user.user_name.replace(" ", "_") == user_name:
                        found_user = user
                        break
                
                if found_user:
                    current_user = found_user
                    logged_in = True
                else:
                    print("Error: Invalid account holder name.")
        
        elif command == "logout":
            if logged_in:
                log_transaction("00_________________________00000_00000.00__")
                print("Logout successful.")
                logged_in = False
                current_user = None
                session_type = None
                break
            else:
                print("You are not logged in.")
        
        elif command == "withdrawal":
            if not logged_in:
                print("Error: You must be logged in to perform transactions.")
                continue
            
            amount = float(input("Enter withdrawal amount: "))
            if session_type == "admin" or (current_user and current_user.balance >= amount):
                if current_user:
                    current_user.balance -= amount
                print(f"Withdrawal successful. New balance: ${current_user.balance:.2f}" if current_user else "Admin withdrawal successful.")
            else:
                print("Error: Insufficient balance.")
        
        elif command == "transfer":
            if not logged_in:
                print("Error: You must be logged in to perform transactions.")
                continue
            
            sender_account = input("Enter sender account number: ").strip()
            receiver_account = input("Enter target account number: ").strip()
            amount = float(input("Enter transfer amount: "))
            
            if session_type == "admin" or (current_user and check.sender_account_match(current_user, sender_account)):
                if receiver_account in USERS and receiver_account != sender_account:
                    transfer = Transfer(session_type, USERS[sender_account], USERS[receiver_account], amount)
                    transfer.process_transfer()
                    # Write transaction output to log file
                    transaction_output = transfer.return_transaction_output()
                    log_transaction(transaction_output)
                    
                else:
                    print("Error: Invalid target account number.")
            else:
                print("Error: Unauthorized transfer. You can only transfer from accounts you own.")
        
        elif command == "paybill":
            if not logged_in:
                print("Error: You must be logged in to perform transactions.")
                continue
            
            sender_account = input("Enter sender account number: ").strip()
            company = input("Enter company code (EC, CQ, FI): ").strip().upper()
            amount = float(input("Enter bill amount: "))
            
            if session_type == "admin" or (current_user and check.sender_account_match(current_user, sender_account)):
                paybill = Paybill(session_type, USERS[sender_account], company, amount)
                paybill.process_paybill()
                # Write transaction output to log file
                company_id = paybill.check.company_id_check(company)
                transaction_output = paybill.return_transaction_output(company_id)
                log_transaction(transaction_output)       
                
            else:
                print("Error: You must be logged in as a standard user to pay bills.")
        
        elif command == "deposit":
            if not logged_in or session_type != "admin":
                print("Error: You must be logged in as an admin to deposit into other accounts.")
                continue

            account_number = input("Enter account number: ").strip()
            account_holder_name = input("Enter account holder name: ").strip()

            if account_number in USERS and USERS[account_number].user_name.strip() == account_holder_name:
                deposit_amount = float(input("Enter deposit amount: "))
                
                if deposit_amount > 0:
                    deposit = Deposit(session_type, USERS[account_number], deposit_amount)
                    deposit.process_deposit()
                    # Log transaction
                    transaction_output = deposit.return_transaction_output()
                    log_transaction(transaction_output)
                else:
                    print("Error: Deposit amount must be greater than zero.")
            else:
                print("Error: Account number and holder name do not match.")
        
        elif command == "create":
            if not logged_in or session_type != "admin":
                print("Error: You must be logged in as an admin to deposit into other accounts.")
                continue
            create_account = Create(session_type, USERS)
            create_account.process_creation()

        elif command == "changeplan":
            if not logged_in:
                print("Error: You must be logged in to perform transactions.")
                continue

            if session_type != "admin":
                print("Error: This is a privileged transaction that requires admin mode.")
                continue

            # Ask for the account holder name
            account_holder_name = input("Enter account holder name: ").strip()

            # Search for a user with the given name.
            found_user = None
            for user in USERS.values():
                if user.user_name.strip().lower() == account_holder_name.lower():
                    found_user = user
                    break

            if found_user is None:
                print("Error: Account holder name not found.")
                continue

            # Ask for the account number.
            account_number = input("Enter account number: ").strip()

            # Now perform the changeplan transaction. The ChangePlan class will check
            # that the provided account number matches the user's actual account number.
            change_plan = ChangePlan(session_type, found_user, account_number)
            change_plan.process_changeplan()

            # Log the transaction output only if the transaction was successful.
            transaction_output = change_plan.return_transaction_output()
            log_transaction(transaction_output)

        elif command == "disable":
            if not logged_in:
                print("Error: You must be logged in to perform transactions.")
                continue

            if session_type != "admin":
                print("Error: This is a privileged transaction that requires admin mode.")
                continue

            # Prompt for the account holder's name.
            account_holder_name = input("Enter account holder name: ").strip()
            # Prompt for the account number.
            account_number = input("Enter account number: ").strip()

            # Create a Disable transaction instance and process it.
            disable_txn = Disable(session_type, account_holder_name, account_number, USERS)
            disable_txn.process_disable()

            # Log the transaction only if processing succeeded.
            transaction_output = disable_txn.return_transaction_output()
            if transaction_output:
                log_transaction(transaction_output)


        else:
            print("Invalid command.")

if __name__ == "__main__":
    banking_system()
