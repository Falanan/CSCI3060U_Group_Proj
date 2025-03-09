from check import Check

class Create:
    """
    A class to handle the creation of new user accounts.
    Only admins can create new accounts.
    """
    def __init__(self, userType, accounts, transaction_file="daily_transaction_file.txt"):
        """
        Initializes the Create class.
        
        :param userType: The type of user (should be 'admin' for account creation).
        :param accounts: A dictionary containing existing accounts.
        :param transaction_file: The file where transaction logs are stored (default: 'daily_transaction_file.txt').
        """
        self.userType = userType  # 'admin' or 'user'
        self.accounts = accounts  # Dictionary containing existing accounts
        self.transaction_file = transaction_file  # File to store transactions
        self.check = Check()

    def process_creation(self):
        """
        Handles the process of creating a new account.
        Ensures the user is an admin and validates input before account creation.
        """
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

        # Generate unique account number (ensures 5-digit format)
        account_number = str(len(self.accounts) + 1).zfill(5)

        # Create the new account entry
        new_account = {
            "account_number": account_number,
            "user_name": account_holder,
            "balance": initial_balance,
            "availability": "A",  # Mark the account as active
        }

        # Add the new account to the accounts dictionary
        self.accounts[account_number] = new_account

        # Log the transaction details
        transaction_output = self.return_transaction_output(new_account, initial_balance)
        self.log_transaction(transaction_output)

        print(f"Account created successfully with account number: {account_number}")

    def return_transaction_output(self, new_account, initial_balance):
        """
        Formats the transaction output string for logging.
        
        :param new_account: The newly created account dictionary.
        :param initial_balance: The initial deposit balance.
        :return: Formatted transaction string.
        """
        formatted_username = new_account["user_name"].replace(" ", "_").ljust(21, "_")
        transaction_output = (
            f"05_{formatted_username}_"
            f"{new_account['account_number']:>5}_"
            f"{float(initial_balance):.2f}"
        )
        return transaction_output

    def log_transaction(self, transaction_output):
        """
        Logs the transaction into the daily transaction file.
        
        :param transaction_output: The formatted transaction string.
        """
        with open(self.transaction_file, "a") as file:
            file.write(transaction_output + "\n")