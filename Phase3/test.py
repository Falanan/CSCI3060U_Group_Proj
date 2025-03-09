"""
Main Banking System

Description:
This program simulates a banking system that allows users to perform transactions such as 
withdrawals, transfers, and bill payments. Users must log in before performing any transaction. 
The system supports both standard (user) and admin sessions, where admin sessions have special 
privileges (e.g., overriding account limits, accessing all user accounts).

Input Sources:
- No dedicated input file for accounts (hardcoded users)
- CLI-based user input for commands

Output File:
- daily_transaction_file.txt: Stores a record of all transactions performed during a session.

How to Run:
1. Execute main.py to start the application.
2. Enter "login" to authenticate:
   - Enter session type ("admin" or "standard").
   - Admin users get full access; standard users enter their account number.
3. After successful login, you can enter one of the following commands:
   - "withdrawal" to withdraw funds.
   - "transfer"  to move funds between accounts.
   - "paybill"   to pay a bill to a known company.
   - "create"    (admin only) to create a new account.
   - "delete"    (admin only) to remove an existing account.
   - "disable"   (admin only) to disable an account.
   - "changeplan" (admin only) to switch or toggle the account’s plan.
   - "logout"    to end the session and save all transactions.
4. Transaction details are automatically written to daily_transaction_file.txt upon each operation.

TODO:
- Enhance error handling for edge cases.
- Implement file-based user accounts instead of hardcoding.
- Break transactions day by day into separate logs.
"""

import sys
from transfer import Transfer
from paybill import Paybill
from check import Check
from deposit import Deposit
from create import Create
from delete import Delete
from changeplan import ChangePlan
from disable import Disable
from login import Login
from withdrawal import Withdrawal
from logout import Logout

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

def get_account(account_number):
    """Retrieve user account details."""
    return USERS.get(account_number)

# # For transaction file
# TRANSACTION_FILE = "daily_transaction_file.txt"

# def log_transaction(transaction):
#     with open(TRANSACTION_FILE, "a") as file:
#         file.write(transaction + "\n")

# def banking_system():
    
def banking_system(input_file, console_output_file, transaction_output_file):
    with open(input_file, "r") as f:
        commands = [line.strip() for line in f.readlines()]

    console_output = []
    transaction_logs = []
    
    logged_in = False
    current_user = None
    session_type = None
    check = Check()
    
    # while True:
    #     command = input("Enter command: ").strip().lower()
    i = 0
    while i < len(commands):
        command = commands[i].lower()
            
        if command == "login":
            # print("Welcome to the banking system.")
            
            # session_type = input("Enter session type: ").strip().lower()
            console_output.append("Welcome to the banking system.")
            session_type = commands[i+1].strip().lower()
            
            if session_type == "admin":
                # login_instance = Login(session_type, None, logged_in)
                # login_instance.process_login()
                console_output.append("Enter session type: admin")
                logged_in = True
                current_user = None
                
                i += 2
                continue
                
            else:
                # account_number = input("Enter account number: ").strip()
                # found_user = USERS.get(account_number)
                
                # if found_user:
                #     current_user = found_user
                #     login_instance = Login(session_type, current_user, logged_in)
                #     login_instance.process_login()
                #     logged_in = True
                # else:
                #     print("Error: Invalid account number.")
                console_output.append("Enter session type: standard")
                enter_user_name = commands[i+2].strip().replace(" ", "_")
                
                found_account = None
                for account_number, user in USERS.items():
                    if user.user_name == enter_user_name:
                        found_account = account_number
                        break
                
                if found_account:
                    current_user = USERS[found_account]
                    logged_in = True
                    console_output.append(f"Enter account holder name: {enter_user_name}")
                else:
                    console_output.append("Error: Invalid account name.")
                
                i += 3
                continue
        
        elif command == "withdraw":
            if not logged_in:
                print("Error: You must be logged in to withdraw.")
                continue
            
            if session_type == "admin":
                account_number = input("Enter account number: ").strip()
                user_name = input("Enter user name: ").strip()
                current_user = USERS.get(account_number)
                if not current_user or current_user.user_name != user_name:
                    print("Error: Invalid account number or user name.")
                    continue
            
            amount = input("Enter withdrawal amount: ").strip()
            try:
                amount = float(amount)
            except ValueError:
                print("Error: Invalid withdrawal amount.")
                continue
            
            withdrawal_instance = Withdrawal(current_user, amount)
            withdrawal_instance.process_withdrawal()
            # withdrawal_output = withdrawal_instance.return_transaction_output()
            # log_transaction(withdrawal_output)
        
        elif command == "transfer":
            if not logged_in:
                # print("Error: You must be logged in to perform transactions.")
                console_output.append("Error: You must be logged in to perform transactions.")
                i += 1
                continue
            
            # sender_account = input("Enter sender account number: ").strip()
            # receiver_account = input("Enter target account number: ").strip()
            # amount = float(input("Enter transfer amount: "))
            sender_account = commands[i+1].strip()
            receiver_account = commands[i+2].strip()
            amount = float(commands[i+3].strip())
            
            if session_type == "admin" or (current_user and check.sender_account_match(current_user, sender_account)):
                if receiver_account in USERS and receiver_account != sender_account:
                    transfer = Transfer(session_type, USERS[sender_account], USERS[receiver_account], amount)
                    success, message = transfer.process_transfer()
                    # # Write transaction output to log file
                    # transaction_output = transfer.return_transaction_output()
                    # log_transaction(transaction_output)
                    console_output.append(message)
                    if success:
                        transaction_logs.append(transfer.return_transaction_output())
                    
            #     else:
            #         print("Error: Invalid target account number.")
            # else:
            #     print("Error: Unauthorized transfer. You can only transfer from accounts you own.")
                else:
                    console_output.append("Error: Invalid target account number.")
            else:
                console_output.append("Error: Unauthorized transfer. You can only transfer from accounts you own.")
        
            i += 4
            continue
        
        elif command == "paybill":
            if not logged_in:
                # print("Error: You must be logged in to perform transactions.")
                console_output.append("Error: You must be logged in to pay bills.")
                i += 1
                continue
            
            # sender_account = input("Enter sender account number: ").strip()
            # company = input("Enter company code (EC, CQ, FI): ").strip().upper()
            # amount = float(input("Enter bill amount: "))
            sender_account = commands[i+1].strip()
            company = commands[i+2].strip()
            amount = float(commands[i+3].strip())
            
            if session_type == "admin" or (current_user and check.sender_account_match(current_user, sender_account)):
                paybill = Paybill(session_type, USERS[sender_account], company, amount)
                success, message = paybill.process_paybill()
                console_output.append(message)
                if success:
                    transaction_logs.append(paybill.return_transaction_output())
                # # Write transaction output to log file
                # company_id = paybill.check.company_id_check(company)
                # transaction_output = paybill.return_transaction_output(company_id)
                # log_transaction(transaction_output)       
                
            else:
                # print("Error: You must be logged in as a standard user to pay bills.")
                console_output.append("Error: You must be logged in as a standard user to pay bills.")
            
            i += 4
            continue
        
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
                    # transaction_output = deposit.return_transaction_output()
                    # log_transaction(transaction_output)
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
        
        elif command == "delete":
            if not logged_in or session_type != "admin":
                print("Error: You must be logged in as an admin to delete accounts.")
                continue
            
            delete_account = Delete(session_type, USERS)
            delete_account.process_deletion()

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
            # transaction_output = change_plan.return_transaction_output()
            # log_transaction(transaction_output)

        elif command == "disable":
            if not logged_in:
                print("Error: You must be logged in to perform transactions.")
                continue

            if session_type != "admin":
                print("Error: This is a privileged transaction that requires admin mode.")
                continue

            # Prompt for the account holder's name.
            account_holder_name = input("Enter account holder name: ").strip()

            # Preliminary check: verify the account holder name exists.
            found_user = None
            for user in USERS.values():
                if user.user_name.strip().lower() == account_holder_name.lower():
                    found_user = user
                    break

            if found_user is None:
                print("Error: Account holder name not found.")
                continue

            # Now prompt for the account number.
            account_number = input("Enter account number: ").strip()

            # Create a Disable transaction instance and process it.
            from disable import Disable
            disable_txn = Disable(session_type, account_holder_name, account_number, USERS)
            disable_txn.process_disable()

            # Log the transaction output if the processing succeeded.
            # transaction_output = disable_txn.return_transaction_output()
            # if transaction_output:
            #     log_transaction(transaction_output)

        elif command == "logout":
        #     # Create a Logout transaction instance.
        #     logout_txn = Logout(logged_in, session_type, current_user)
            
        #     # Process logout; if successful, log the transaction and clear session state.
        #     if logout_txn.process_logout():
        #         # transaction_output = logout_txn.return_transaction_output()
        #         # log_transaction(transaction_output)
        #         logged_in = False
        #         current_user = None
        #         session_type = None

        # else:
        #     print("Invalid command.")
            if logged_in:
                logout_txn = Logout(logged_in, session_type, current_user)
                success, message, transaction_record = logout_txn.process_logout()
                console_output.append(message)
                if success:
                    transaction_logs.append(transaction_record)

                logged_in = False
                session_type = None
                current_user = None
            else:
                console_output.append("Error: No active session to logout.")
            
            i += 1
            continue
        i += 1
    # Write console output to .out file
    with open(console_output_file, "w") as f:
        f.write("\n".join(console_output) + "\n")

    # Write transaction output to .etf file
    with open(transaction_output_file, "w") as f:
        for record in transaction_logs:
            f.write(record + "\n")

    print("Transaction processing completed.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <input_file> <console_output_file> <transaction_output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    console_output_file = sys.argv[2]
    transaction_output_file = sys.argv[3]

    banking_system(input_file, console_output_file, transaction_output_file)

# if __name__ == "__main__":
#     banking_system()
