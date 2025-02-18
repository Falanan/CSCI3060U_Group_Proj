from check import Check

class Create:
    def __init__(self, userType, accounts, transaction_file="daily_transaction_file.txt"):
        self.userType = userType  # 'admin' or 'user'
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

    def return_transaction_output(self, new_account, initial_balance):
        # Prepare the transaction output in the required format
        formatted_username = new_account["user_name"].replace(" ", "_").ljust(21, "_")
        transaction_output = (
            f"05_{formatted_username}_"
            f"{new_account['account_number']:>5}_"
            f"{float(initial_balance):.2f}"
        )
        return transaction_output

    def log_transaction(self, transaction_output):
        # Log the transaction to the daily transaction file
        with open(self.transaction_file, "a") as file:
            file.write(transaction_output + "\n")