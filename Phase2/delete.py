from check import Check

class Delete:
    """
    This class handles the deletion of user accounts. 
    Only administrators are allowed to delete accounts.
    """

    def __init__(self, userType, accounts, transaction_file="daily_transaction_file.txt"):
        """
        Initializes the Delete class.

        Parameters:
        - userType (str): Specifies whether the user is an 'admin' or 'user'.
        - accounts (dict): Dictionary containing existing accounts.
        - transaction_file (str): File where transactions are logged (default: "daily_transaction_file.txt").
        """
        self.userType = userType  # Role of the user performing the deletion
        self.accounts = accounts  # Dictionary of accounts (account_number -> account object)
        self.transaction_file = transaction_file  # File to log transactions
        self.check = Check()  # Instance of Check class for validation purposes

    def process_deletion(self):
        """
        Handles the account deletion process.

        Steps:
        1. Ensures that only an admin can delete accounts.
        2. Takes input for the account holder's name and account number.
        3. Checks if the provided account exists and belongs to the entered user.
        4. If valid, logs the deletion transaction and removes the account.
        """

        # Ensure only admins can delete accounts
        if self.userType != "admin":
            print("Error: Only admins can delete accounts.")
            return

        # Ask for the account holder's name
        account_holder = input("Enter the account holder's name: ").strip()
        
        # Ask for the account number
        account_number = input("Enter the account number: ").strip()
        
        # Validate input
        if not account_holder:
            print("Error: Account holder name cannot be empty.")
            return

        # Check if the account exists and matches the provided account holder's name
        account_found = None
        if account_number in self.accounts and self.accounts[account_number].user_name.strip() == account_holder:
            account_found = self.accounts[account_number]
        
        # If no matching account is found, print an error message
        if not account_found:
            print(f"Error: No account found for {account_holder} with account number {account_number}.")
            return

        # Save the deletion transaction to the file
        transaction_output = self.return_transaction_output(account_found)
        self.log_transaction(transaction_output)

        # Remove the account from the dictionary
        del self.accounts[account_number]

        print(f"Account with account number {account_number} has been deleted successfully.")

    def return_transaction_output(self, deleted_account):
        """
        Formats the transaction output for logging.

        Parameters:
        - deleted_account (dict): The account that is being deleted.

        Returns:
        - str: A formatted transaction string representing the deletion.
        """

        # Format the username for consistent length and format
        formatted_username = deleted_account.user_name.replace(" ", "_").ljust(21, "_")

        # Format the transaction output according to the required format
        transaction_output = (
            f"06_{formatted_username}_"
            f"{deleted_account.account_number:>5}_"
            f"00000.00__"  # Zero balance since the account is deleted
        )
        return transaction_output

    def log_transaction(self, transaction_output):
        """
        Logs the transaction details to the daily transaction file.

        Parameters:
        - transaction_output (str): The formatted transaction string to be recorded.
        """

        # Append the transaction details to the transaction log file
        with open(self.transaction_file, "a") as file:
            file.write(transaction_output + "\n")