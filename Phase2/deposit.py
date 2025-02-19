from check import Check

class Deposit:
    """
    This class handles deposit transactions for a user's account.
    It ensures proper validation of the deposit amount and account status
    before processing the transaction.
    """
    def __init__(self, userType, user, amount=None):
        """
        Initializes the Deposit class with user type, user details, and deposit amount.
        
        :param userType: str - Specifies whether the user is an 'admin' or a 'user'.
        :param user: User object - Contains user account details.
        :param amount: float (optional) - The amount to be deposited.
        """
        self.userType = userType  # 'admin' or 'user'
        self.user = user  # User object with account details
        self.amount = amount  # Amount to be deposited
        self.check = Check()  # Instance of Check class for validation

    def process_deposit(self):
        """
        Processes the deposit by performing multiple validation checks
        and updating the user's balance if valid.
        
        :return: str - Formatted transaction output if successful, else None.
        """
        # Validate input fields
        all_inputs_valid, missing_fields = self.check.missing_input_check(
            user=self.user,
            amount=self.amount
        )
        if not all_inputs_valid:
            print(f"Error: The deposit {', '.join(missing_fields)} is missing, so the process will be rejected. Please re-try.")
            return
        
        # Validate deposit amount
        if not self.check.invalid_character_check(self.amount):
            print("Error: Invalid deposit amount. Amount must be numeric.")
            return
        if not self.check.negative_amount_check(self.amount):
            print("Error: Invalid deposit amount. Amount must be positive.")
            return
        if not self.check.zero_amount_check(self.amount):
            print("Error: Deposit amount must be greater than zero.")
            return

        # Check if the account is active
        if not self.check.availability_check(self.user):
            print("Error: Account is inactive. Please use an available account.")
            return

        # Process the deposit by updating the balance
        self.user.balance += self.amount
        print(f"Deposit successful. New balance: ${self.user.balance:.2f}")

        # Generate and return transaction log entry
        transaction_output = self.return_transaction_output()
        return transaction_output  # Return this so main.py can log it

    def return_transaction_output(self):
        """
        Generates a formatted transaction output string for logging purposes.
        
        :return: str - Formatted transaction string.
        """
        formatted_username = self.user.user_name.replace(" ", "_").ljust(21, "_")
        transaction_output = (
            f"04_{formatted_username}_"
            f"{self.user.account_number:>5}_"
            f"{float(self.amount):.2f}"
        )
        return transaction_output
