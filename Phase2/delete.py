from check import Check

class Delete:
    def __init__(self, userType, accounts, transaction_file="daily_transaction_file.txt"):
        self.userType = userType  # 'admin' or 'user'
        self.accounts = accounts  # Dictionary containing existing accounts
        self.transaction_file = transaction_file  # File to store transactions
        self.check = Check()

    def process_deletion(self):
        # Ensure only admins can delete accounts
        if self.userType != "admin":
            print("Error: Only admins can delete accounts.")
            return

        # Ask for the account holder's name
        account_holder = input("Enter the account holder's name: ").strip()
        # Ask for the account number
        account_number = input("Enter the account number: ").strip()
        if not account_holder:
            print("Error: Account holder name cannot be empty.")
            return
        
        # Check if the account holder exists
        account_found = None
        if account_number in self.accounts and self.accounts[account_number].user_name.strip() == account_holder:
            account_found = self.accounts[account_number]
        
        if not account_found:
            print(f"Error: No account found for {account_holder} with account number {account_number}.")
            return

        # Save the deletion transaction to the file
        transaction_output = self.return_transaction_output(account_found)
        self.log_transaction(transaction_output)

        print(f"Account with account number {account_number} has been deleted successfully.")

    def return_transaction_output(self, deleted_account):
        # Prepare the transaction output in the required format
        formatted_username = deleted_account.user_name.replace(" ", "_").ljust(21, "_")
        transaction_output = (
            f"06_{formatted_username}_"
            f"{deleted_account.account_number:>5}_"
            f"00000.00__"
        )
        return transaction_output

    def log_transaction(self, transaction_output):
        # Log the transaction to the daily transaction file
        with open(self.transaction_file, "a") as file:
            file.write(transaction_output + "\n")