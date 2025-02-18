# from check import Check

# class Create:
#     def __init__(self, userType, accounts):
#         self.userType = userType  # 'admin' or 'standard'
#         self.accounts = accounts  # Dictionary containing existing accounts
#         self.check = Check()

#     def process_creation(self):
#         # Ensure only admins can create an account
#         if self.userType != "admin":
#             print("Error: Only admins can create new accounts.")
#             return

#         # Get the account holder's name
#         account_holder = input("Enter the account holder's name: ").strip()
#         if not account_holder:
#             print("Error: Account holder name cannot be empty.")
#             return
#         if len(account_holder) > 20:
#             print("Error: Account holder name must be at most 20 characters.")
#             return

#         # Get the initial balance
#         try:
#             initial_balance = float(input("Enter the initial balance: ").strip())
#         except ValueError:
#             print("Error: Invalid balance. Please enter a numeric value.")
#             return

#         # Validate balance
#         if not self.check.negative_amount_check(initial_balance):
#             print("Error: Balance cannot be negative.")
#             return
#         if initial_balance > 99999.99:
#             print("Error: Initial balance cannot exceed $99999.99.")
#             return

#         # Generate a unique account number
#         new_account_number = self.generate_account_number()
#         if not new_account_number:
#             print("Error: Could not generate a unique account number.")
#             return

#         # Save the new account (but it will not be available in this session)
#         self.accounts[new_account_number] = {
#             "account_holder": account_holder,
#             "balance": initial_balance,
#             "active": False  # Mark as unavailable for this session
#         }

#         print(f"Account successfully created. Account Number: {new_account_number}")

#         # Save the transaction
#         self.display_transaction_output(new_account_number, account_holder, initial_balance)

#     def generate_account_number(self):
#         """Generates a unique 5-digit account number."""
#         existing_numbers = {int(acc_num) for acc_num in self.accounts.keys()}
#         for num in range(1, 100000):  # Valid account numbers: 00001 - 99999
#             if num not in existing_numbers:
#                 return f"{num:05d}"  # Ensure 5-digit formatting
#         return None  # No available account numbers

#     def return_transaction_output(self, account_number, account_holder, balance):
#         formatted_name = account_holder.replace(" ", "_").ljust(21, "_")
#         transaction_output = (
#             f"05_{formatted_name}_"
#             f"{account_number:>5}_"
#             f"{float(balance):.2f}"
#         )
#         return transaction_output

from check import Check

class Create:
    def __init__(self, userType, accounts, transaction_file="daily_transaction_file.txt"):
        self.userType = userType  # 'admin' or 'standard'
        self.accounts = accounts  # Dictionary containing existing accounts
        self.transaction_file = transaction_file  # File to store transactions
        self.check = Check()

    def process_creation(self):
        # Ensure only admins can create an account
        if self.userType != "admin":
            print("Error: Only admins can create new accounts.")
            return

        # Get the account holder's name
        account_holder = input("Enter the account holder's name: ").strip()
        if not account_holder:
            print("Error: Account holder name cannot be empty.")
            return
        if len(account_holder) > 20:
            print("Error: Account holder name must be at most 20 characters.")
            return

        # Get the initial balance
        try:
            initial_balance = float(input("Enter the initial balance: ").strip())
        except ValueError:
            print("Error: Invalid balance. Please enter a numeric value.")
            return

        # Validate balance
        if not self.check.negative_amount_check(initial_balance):
            print("Error: Balance cannot be negative.")
            return
        if initial_balance > 99999.99:
            print("Error: Initial balance cannot exceed $99,999.99.")
            return

        # Generate unique account number
        account_number = str(len(self.accounts) + 1).zfill(5)  # Generate a 5-digit account number

        # Create the new account
        new_account = {
            "account_number": account_number,
            "user_name": account_holder,
            "balance": initial_balance,
            "availability": "A",  # Mark the account as active
        }

        # Add the new account to the accounts dictionary
        self.accounts[account_number] = new_account

        # Write the transaction to the transaction file
        transaction_output = self.return_transaction_output(new_account, initial_balance)
        self.log_transaction(transaction_output)

        print(f"Account created successfully with account number: {account_number}")
        print(transaction_output)

    def return_transaction_output(self, new_account, initial_balance):
        # Prepare the transaction output in the required format
        formatted_username = new_account["user_name"].replace(" ", "_").ljust(21, "_")
        transaction_output = (
            f"01_{formatted_username}_"
            f"{new_account['account_number']:>5}_"
            f"{float(initial_balance):.2f}"
        )
        return transaction_output

    def log_transaction(self, transaction_output):
        # Log the transaction to the daily transaction file
        with open(self.transaction_file, "a") as file:
            file.write(transaction_output + "\n")