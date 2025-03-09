
"""
Paybill Class

Handles the payment of bills to predefined companies. 
This class ensures proper validation of inputs, available funds, and transaction limits.
"""

from check import Check

class Paybill:
    
    """
    Handles bill payments, ensuring the user has sufficient balance and the biller is valid.
    """
    
    COMPANY_ACCOUNTS = {
        "EC": "10000",
        "CQ": "20000",
        "FI": "30000"
    }

    def __init__(self, userType, user, company, amount = None, limit=2000.00, write_console=None):
        self.userType = userType
        self.user = user
        self.company = company
        self.amount = amount
        self.limit = limit
        self.check = Check()
        
        # Provide a default no-op if not given
        if write_console is None:
            def _default_console(msg): pass
            self.write_console = _default_console
        else:
            self.write_console = write_console

    def process_paybill(self):
        """ Processes the bill payment after performing necessary validations. """
        # Basic checks
        all_inputs_valid, missing_fields = self.check.missing_input_check(
            user=self.user, 
            company=self.company, 
            amount=self.amount
        )
        if not all_inputs_valid:
            # print(f"Error: The paybill {', '.join(missing_fields)} is missing, so the process will be rejected. Please re-try.")
            self.write_console(f"Error: The paybill {', '.join(missing_fields)} is missing, so the process will be rejected. Please re-try.")
            return
        
        if not self.check.invalid_character_check(self.amount):
            # print("Error: Invalid payment amount. Amount must be numeric.")
            self.write_console("Error: Invalid payment amount. Amount must be numeric.")
            return
        
        if not self.check.valid_company_check(self.company):
            # print(f"Error: '{self.company}' is not a recognized biller. Please use EC, CQ, or FI.")
            self.write_console(f"Error: '{self.company}' is not a recognized biller. Please use EC, CQ, or FI.")
            return
        
        company_id = self.check.company_id_check(self.company)
        if not company_id:
            # print("Error: No valid company ID found for the selected biller.")
            self.write_console("Error: No valid company ID found for the selected biller.")
            return

        # If user is admin, skip paybill limit & ownership checks, but still do negative/zero/funds checks
        if self.userType == "admin":
            # Admin override
            if not self.check.negative_amount_check(self.amount):
                # print("Error: Invalid payment amount. Amount must be positive.")
                self.write_console("Error: Invalid payment amount. Amount must be positive.")
                return
            
            if not self.check.zero_amount_check(self.amount):
                # print("Error: Payment amount must be greater than zero.")
                self.write_console("Error: Payment amount must be greater than zero.")
                return
            
            if not self.check.balance_check(self.user, self.amount):
                # print(f"Insufficient funds to pay the bill. Available balance: ${self.user.balance}.")
                self.write_console(f"Error: Insufficient funds to pay the bill. Available balance: ${self.user.balance:,.2f}")
                return

            # Assume admin able to pay from disabled accounts
            # if not self.check.availability_check(self.user):
            #     print(f"Error: Account {self.user.account_number} is inactive. Payment cannot be processed.")
            #     return

            self.user.balance -= self.amount
            # print(f"Payment successful. New balance for Account {self.user.account_number}: ${self.user.balance:.2f} .")
            # self.display_transaction_output(company_id)
            self.write_console(
                f"Payment successful. New balance for Account {self.user.account_number}: "
                f"${self.user.balance:,.2f}."
            )
            return

        # Standard user checks
        # if not self.check.availability_check(self.user):
        #     print("Error: Your account is disabled. Please use an available account to paybill.")
        #     return
        # if not self.check.negative_amount_check(self.amount):
        #     print("Error: Invalid payment amount. Amount must be positive.")
        #     return
        # if not self.check.zero_amount_check(self.amount):
        #     print("Error: Payment amount must be greater than zero.")
        #     return
        # if not self.check.limit_check(self.amount, self.limit):
        #     print(f"Error: Maximum bill payment limit exceeded. You can pay up to ${self.limit:.2f} in this session.")
        #     return
        # if not self.check.balance_check(self.user, self.amount):
        #     print(f"Insufficient funds to pay the bill. Available balance: ${self.user.balance}.")
        #     return
        # if not self.company_check():
        #     print("Error: Biller not recognized. Please use EC, CQ, or FI.")
        #     return

        # # Process standard paybill
        # self.user.balance -= self.amount
        # print(f"Payment successful. New balance for Account {self.user.account_number}: ${self.user.balance:.2f} .")
        # self.display_transaction_output(company_id)
        if not self.check.availability_check(self.user):
                self.write_console("Error: Your account is disabled. Please use an available account to paybill.")
                return
        if not self.check.negative_amount_check(self.amount):
            self.write_console("Error: Invalid payment amount. Amount must be positive.")
            return
        if not self.check.zero_amount_check(self.amount):
            self.write_console("Error: Payment amount must be greater than zero.")
            return
        if not self.check.limit_check(self.amount, self.limit):
            self.write_console(f"Error: Maximum bill payment limit exceeded. You can pay up to ${self.limit:.2f} in this session.")
            return
        if not self.check.balance_check(self.user, self.amount):
            self.write_console(f"Insufficient funds to pay the bill. Available balance: ${self.user.balance}.")
            return
        if not self.company_check():
            self.write_console("Error: Biller not recognized. Please use EC, CQ, or FI.")
            return

        self.user.balance -= self.amount
        self.write_console(
            f"Payment successful. New balance for Account {self.user.account_number}: "
            f"${self.user.balance:,.2f}."
        )

    def company_check(self):
        return self.company in self.COMPANY_ACCOUNTS

    # def display_transaction_output(self, company_id):
    #     """ Displays the formatted transaction output for logging. """
    #     formatted_username = self.user.user_name.replace(" ", "_").ljust(21, "_")
    #     transaction_output = (
    #         f"03_{formatted_username}_"
    #         f"{self.user.account_number:>5}_"
    #         f"{float(self.amount):.2f}_"
    #         f"{company_id}"
    #     )
    #     end_session_output = "00_________________________00000_00000.00__" 

    #     print(transaction_output)
    #     print(end_session_output)
    
    def return_transaction_output(self, company_id):
        """ Returns the formatted transaction output for logging. """
        formatted_username = self.user.user_name.replace(" ", "_").ljust(21, "_")
        transaction_output = (
            f"03_{formatted_username}_"
            f"{self.user.account_number:>5}_"
            f"{float(self.amount):.2f}_"
            f"{company_id}\n"
        )
        return transaction_output
