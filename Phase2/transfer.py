from check import Check

class Transfer:
    def __init__(self, userType, user1, user2, amount = None, limit=1000.00):
        self.userType = userType
        self.user1 = user1
        self.user2 = user2
        self.amount = amount
        self.limit = limit
        self.check = Check()

    def process_transfer(self):
        # Check for missing inputs
        all_inputs_valid, missing_fields = self.check.missing_input_check(
            user1=self.user1,
            user2=self.user2,
            amount=self.amount
        )
        if not all_inputs_valid:
            print(f"Error: The paybill {', '.join(missing_fields)} is missing, so the process will be rejected. Please re-try.")
            return
        
        # Basic checks that should always run
        if not self.check.account_existence_check(self.user2):
            print("Error: Target account does not exist.")
            return
        if not self.check.invalid_character_check(self.amount):
            print("Error: Invalid transfer amount. Amount must be numeric.")
            return

        # If admin, skip ownership & limit checks, but still check negative/zero amounts & funds
        if self.userType == "admin":
            # Admin override
            # Admin can transfer from any account to any other account, ignoring limit & ownership
            if not self.check.negative_amount_check(self.amount):
                print("Error: Invalid transfer amount. Amount must be positive.")
                return
            if not self.check.zero_amount_check(self.amount):
                print("Error: Transfer amount must be greater than zero.")
                return
            if not self.check.balance_check(self.user1, self.amount):
                print(f"Error: Insufficient funds for transfer.")
                return

            # Assume admin can transfer from an inactive account if desired
            # if not self.check.availability_check(self.user1):
            #     print("Error: Source account is inactive. Transfer cannot be processed.")
            #     return

            if not self.check.availability_check(self.user2):
                print(f"Error: Account {self.user2.account_number} is disabled. Transfers cannot be processed.")
                return

            # Perform admin transfer
            self.user1.balance -= self.amount
            self.user2.balance += self.amount
            print(f"Transfer successful. New balance: ${self.user1.balance:.2f} (Account {self.user1.account_number}), ${self.user2.balance:.2f} (Account {self.user2.account_number})")
            self.display_transaction_output()

        else:
            # Standard user checks
            if not self.check.user_check(self.user1, self.user2):
                print("Error: Cannot transfer money to the same account.")
                return
            if not self.check.availability_check(self.user1):
                print(f"Error: Account {self.user1.account_number} is disabled. Transfers cannot be processed.")
                return
            if not self.check.availability_check(self.user2):
                print(f"Error: Account {self.user2.account_number} is disabled. Transfers cannot be processed.")
                return
            if not self.check.negative_amount_check(self.amount):
                print("Error: Invalid transfer amount.")
                return
            if not self.check.zero_amount_check(self.amount):
                print("Error: Transfer amount must be greater than zero.")
                return
            if not self.check.limit_check(self.amount, self.limit):
                print(f"Error: Maximum transfer limit exceeded. You can transfer up to ${self.limit:.2f} in this session.")
                return
            if not self.check.balance_check(self.user1, self.amount):
                print("Error: Insufficient funds for transfer.")
                return

            # Process standard transfer
            self.user1.balance -= self.amount
            self.user2.balance += self.amount
            print(f"Transfer successful. New balance: ${self.user1.balance:.2f}.")
            self.display_transaction_output()

    def display_transaction_output(self):
        formatted_username = self.user1.user_name.replace(" ", "_").ljust(21, "_")
        transaction_output = (
            f"02_{formatted_username}_"
            f"{self.user1.account_number:>5}_"
            f"{float(self.amount):.2f}_"
            f"{self.user2.account_number}"
        )

        print(transaction_output)
        
        end_session_output = "00_________________________00000_00000.00__"
        print(end_session_output)
        
    def return_transaction_output(self):
        formatted_username = self.user1.user_name.replace(" ", "_").ljust(21, "_")
        transaction_output = (
            f"02_{formatted_username}_"
            f"{self.user1.account_number:>5}_"
            f"{float(self.amount):.2f}_"
            f"{self.user2.account_number}"
        )

        return transaction_output
    

