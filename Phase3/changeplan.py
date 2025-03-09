from check import Check

class ChangePlan:
    """
    ChangePlan class to handle changing the transaction payment plan for a bank account.
    This transaction toggles the account's plan from Student Plan (SP) to Non-Student Plan (NP)
    (or vice versa) or sets it explicitly. It is a privileged transaction and must be executed
    in admin mode.
    
    Transaction output format (fixed-length, 40 chars):
      CC_AAAAAAAAAAAAAAAAAAAA_NNNNN_PPPPPPPP_MM
    where:
      - CC = "08" for changeplan
      - AAAAAAAAAAAAAAAAAAAA = account holder's name (left-justified, padded)
      - NNNNN = 5-digit account number
      - PPPPPPPP = "00000.00" (since no funds are moved)
      - MM = new plan ("SP" or "NP")
    """

    def __init__(self, userType, user, provided_account_number, new_plan=None):
        """
        :param userType: "admin" or "standard" (must be admin for this transaction)
        :param user: The User object whose plan we are changing
        :param provided_account_number: The account number provided as input
        :param new_plan: Optional. The desired new plan "SP" or "NP". If None, toggles the current plan.
        """
        self.userType = userType
        self.user = user
        self.provided_account_number = provided_account_number
        self.new_plan = new_plan
        self.check = Check()

    def process_changeplan(self):
        """Performs checks and changes the user's plan if valid."""
        if self.userType != "admin":
            print("Error: Change plan transaction requires admin privileges.")
            return

        if not self.check.account_existence_check(self.user):
            print("Error: Account does not exist.")
            return

        if not self.check.availability_check(self.user):
            print(f"Error: Account {self.user.account_number} is disabled. Cannot change plan.")
            return

        # Check if provided account number matches the user's actual account number.
        if self.user.account_number != self.provided_account_number:
            print("Error: The account number does not match the account holder name.")
            return

        # Get the current plan; if not set, assume 'SP'
        current_plan = getattr(self.user, 'plan', 'SP')
        
        # Determine the new plan (toggle if none provided)
        if self.new_plan is None:
            new_plan = "NP" if current_plan == "SP" else "SP"
        else:
            if self.new_plan not in ["SP", "NP"]:
                print("Error: Invalid plan provided. Must be 'SP' or 'NP'.")
                return
            new_plan = self.new_plan

        # Update the user's plan.
        self.user.plan = new_plan
        print(f"Plan change successful. New plan for account {self.user.account_number} is {new_plan}.")

    def return_transaction_output(self):
        """
        Returns the fixed-length string for logging:
        08_{username padded}_NNNNN_00000.00_{plan}
        """
        formatted_username = self.user.user_name.replace(" ", "_").ljust(21, "_")
        plan = getattr(self.user, 'plan', 'SP')
        transaction_output = f"08_{formatted_username}_{self.user.account_number:>5}_00000.00_{plan}"
        return transaction_output
