# from user import User
from check import Check

class Transfer:
    def __init__(self, user1, user2, amount, limit=1000.00):
        self.user1 = user1
        self.user2 = user2
        self.amount = amount
        self.limit = limit
        self.check = Check()

    def process_transfer(self):
        # Perform checks
        if not self.check.account_existence_check(self.user2):
            print("Error: Target account does not exist.")
            return
        if not self.check.invalid_character_check(self.amount):
            print("Error: Invalid transfer amount. Please enter a numeric value.")
            return
        all_inputs_valid, error_message = self.check.missing_input_check(
        user1=self.user1, 
        user2=self.user2, 
        amount=self.amount
        )
        if not all_inputs_valid:
            print(error_message)
            return
        if not self.check.user_check(self.user1, self.user2):
            print("Error: Unauthorized transfer.")
            return
        if not self.check.availability_check(self.user1):
            print("Error: Account is inactive. Transfers cannot be processed.")
            return
        if not self.check.availability_check(self.user2):
            print("Error: Target account is inactive. Transfers cannot be processed.")
            return
        if not self.check.negative_amount_check(self.amount):
            print("Error: Invalid transfer amount. Amount must be positive.")
            return
        if not self.check.zero_amount_check(self.amount):
            print("Error: Transfer amount must be greater than zero.")
            return
        if not self.check.limit_check(self.amount, self.limit):
            print(f"Error: Maximum transfer limit exceeded. You can transfer up to ${self.limit:.2f}.")
            return
        if not self.check.balance_check(self.user1, self.amount):
            print("Error: Insufficient funds for transfer.")
            return

        # Process transfer
        self.user1.balance -= self.amount
        self.user2.balance += self.amount

        print(f"Transfer successful. New balance: ${self.user1.balance:.2f} (Account {self.user1.account_number}), ${self.user2.balance:.2f} (Account {self.user2.account_number}).")
        self.display_transaction_output()

    def display_transaction_output(self):
        transaction_output = f"02_{self.user1.userName:<20}{self.user1.account_number:>5}_{self.amount:08.2f}_{self.user2.account_number}"
        print(transaction_output)
