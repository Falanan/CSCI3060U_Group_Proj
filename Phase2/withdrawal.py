# Test withdrawal 
from check import Check


class Withdrawal:
    def __init__(self, user, amount):
        self.user = user  # User object
        self.amount = amount  # Amount to be withdrawn
        self.check = Check()

    def process_withdrawal(self):
        # Basic input validation
        all_inputs_valid, missing_fields = self.check.missing_input_check(
            user=self.user,
            amount=self.amount
        )
        if not all_inputs_valid:
            print(f"Error: The withdrawal {', '.join(missing_fields)} is missing, so the process will be rejected. Please re-try.")
            return
        if not self.check.invalid_character_check(self.amount):
            print("Error: Invalid withdrawal amount. Amount must be numeric.")
            return
        if not self.check.negative_amount_check(self.amount):
            print("Error: Invalid withdrawal amount. Amount must be positive.")
            return
        if not self.check.zero_amount_check(self.amount):
            print("Error: Withdrawal amount must be greater than zero.")
            return
        if not self.check.balance_check(self.user, self.amount):
            print("Error: Account balance less than requested withdrawal amount.")
            return

        # Process withdrawal
        self.user.balance -= self.amount
        print(f"Withdrawal successful. New balance: ${self.user.balance:.2f}")
        return self.return_transaction_output()
    
    def return_transaction_output(self):
        formatted_username = self.user.user_name.replace(" ", "_").ljust(21, "_")
        transaction_output = (
            f"02_{formatted_username}_"
            f"{self.user.account_number:>5}_"
            f"{float(self.amount):.2f}"
        )
        return transaction_output
    
    def return_transaction_output(self):
        formatted_username = self.user.user_name.replace(" ", "_").ljust(21, "_")
        transaction_output = (
            f"03_{formatted_username}_"
            f"{self.user.account_number:>5}_"
            f"{float(self.amount):.2f}"
        )
        return transaction_output
