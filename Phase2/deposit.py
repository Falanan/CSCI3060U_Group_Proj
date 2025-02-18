from check import Check

class Deposit:
    def __init__(self, userType, user, amount=None):
        self.userType = userType  # 'admin' or 'standard'
        self.user = user  # User object with account details
        self.amount = amount  # Amount to be deposited
        self.check = Check()

    def process_deposit(self):
        # Basic input validation
        all_inputs_valid, missing_fields = self.check.missing_input_check(
            user=self.user,
            amount=self.amount
        )
        if not all_inputs_valid:
            print(f"Error: The deposit {', '.join(missing_fields)} is missing, so the process will be rejected. Please re-try.")
            return
        if not self.check.invalid_character_check(self.amount):
            print("Error: Invalid deposit amount. Amount must be numeric.")
            return
        if not self.check.negative_amount_check(self.amount):
            print("Error: Invalid deposit amount. Amount must be positive.")
            return
        if not self.check.zero_amount_check(self.amount):
            print("Error: Deposit amount must be greater than zero.")
            return

        # Validate that the account exists and is active
        if not self.check.availability_check(self.user):
            print("Error: Account is inactive. Please use an available account.")
            return

        # Process the deposit
        self.user.balance += self.amount
        print(f"Deposit successful. New balance: ${self.user.balance:.2f}")

        # Save the transaction details
        transaction_output = self.return_transaction_output()
        return transaction_output  # Return this so main.py can log it

    def return_transaction_output(self):
        formatted_username = self.user.user_name.replace(" ", "_").ljust(21, "_")
        transaction_output = (
            f"04_{formatted_username}_"
            f"{self.user.account_number:>5}_"
            f"{float(self.amount):.2f}"
        )
        return transaction_output