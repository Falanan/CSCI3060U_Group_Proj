from check import Check

class Disable:
    """
    Disable class to handle disabling a bank account.
    This transaction sets the account's status from active (A) to disabled (D)
    and is a privileged transaction (admin only).
    
    Transaction output format (fixed-length, 40 chars):
      CC_AAAAAAAAAAAAAAAAAAAA_NNNNN_PPPPPPPP_MM
    where:
      - CC = "07" for disable
      - AAAAAAAAAAAAAAAAAAAA = account holder's name (left-justified, padded)
      - NNNNN = 5-digit account number (right-justified)
      - PPPPPPPP = "00000.00" (since no funds are involved)
      - MM = new status ("D")
    """

    def __init__(self, userType, provided_account_holder, provided_account_number, users):
        """
        :param userType: Session type; must be "admin" for this transaction.
        :param provided_account_holder: The account holder name provided by the user.
        :param provided_account_number: The account number provided by the user.
        :param users: Dictionary of User objects keyed by account number.
        """
        self.userType = userType
        self.provided_account_holder = provided_account_holder
        self.provided_account_number = provided_account_number
        self.users = users
        self.check = Check()
        self.user = None  # This will be set to the actual User object after lookup.

    def process_disable(self):
        """Performs checks and disables the account if all validations pass."""
        # Check admin privileges
        if self.userType != "admin":
            print("Error: Disable transaction requires admin privileges.")
            return

        # Lookup user by the provided account holder name.
        found_user = None
        for user in self.users.values():
            if user.user_name.strip().lower() == self.provided_account_holder.lower():
                found_user = user
                break

        if found_user is None:
            print("Error: Account holder name not found.")
            return

        # Check if the provided account number matches the account found.
        if found_user.account_number != self.provided_account_number:
            print("Error: Provided account number does not match the account holder name.")
            return

        self.user = found_user  # Set the user for future use

        # Check if the account is already disabled.
        if not self.check.availability_check(self.user):
            print(f"Error: Account {self.user.account_number} is already disabled.")
            return

        # Disable the account by setting its availability to "D".
        self.user.availability = "D"
        print(f"Account {self.user.account_number} ({self.user.user_name}) has been disabled.")

    def return_transaction_output(self):
        """
        Returns the fixed-length transaction output string for a disable transaction:
        07_{username padded}_NNNNN_00000.00_D
        """
        if self.user is None:
            # If the transaction did not process correctly, return an empty string.
            return ""
        formatted_username = self.user.user_name.replace(" ", "_").ljust(21, "_")
        transaction_output = f"07_{formatted_username}_{self.user.account_number:>5}_00000.00_D"
        return transaction_output
