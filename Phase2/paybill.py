# from user import User
from check import Check

class Paybill:

    def __init__(self, user, company, amount, limit=2000.00):
        self.user = user
        self.company = company
        self.amount = amount
        self.limit = limit
        self.check = Check()

    def process_paybill(self):
        # Perform checks
        all_inputs_valid, error_message = self.check.missing_input_check(
            user=self.user, 
            company=self.company, 
            amount=self.amount
        )
        if not all_inputs_valid:
            print(error_message)
            return
        if not self.check.valid_company_check(self.company):
            print(f"Error: '{self.company}' is not a recognized biller. Please use EC, CQ, or FI.")
            return
        company_id = self.check.company_id_check(self.company)
        if not company_id:
            print("Error: No valid company ID found for the selected biller.")
            return
        # if not self.check.availability_check(self.user):
        #     print("Error: Target account is inactive. Paybill cannot be processed.")
        #     return
        if not self.check.invalid_character_check(self.amount):
            print("Error: Invalid payment amount. Please enter a numeric value.")
            return
        if not self.check.availability_check(self.user):
            print("Error: Your account is disabled. Please use an available account to paybill.")
            return
        if not self.check.negative_amount_check(self.amount):
            print("Error: Invalid payment amount. Amount must be positive.")
            return
        if not self.check.zero_amount_check(self.amount):
            print("Error: Payment amount must be greater than zero.")
            return
        if not self.check.limit_check(self.amount, self.limit):
            print(f"Error: Maximum bill payment limit exceeded. You can pay up to ${self.limit:.2f}.")
            return
        if not self.check.balance_check(self.user, self.amount):
            print("Error: Insufficient funds to pay the bill.")
            return
        if not self.company_check():
            print("Error: Biller not recognized. Please use EC, CQ, or FI.")
            return

        # Process bill payment
        company_id = self.COMPANY_ACCOUNTS[self.company]
        self.user.balance -= self.amount

        print(f"Payment successful. New balance: ${self.user.balance:.2f}.")
        self.display_transaction_output(company_id)

    def company_check(self):
        return self.company in self.COMPANY_ACCOUNTS

    def display_transaction_output(self, company_id):
        transaction_output = f"03_{self.user.userName:<20}{self.user.account_number:>5}_{self.amount:08.2f}_{company_id}"
        print(transaction_output)
