# Test Login

from check import Check

class Login:
    def __init__(self, userType, user):
        self.userType = userType  # 'admin' or 'standard'
        self.user = user  # User object with account details
        self.check = Check()

    def process_login(self):
        # Basic input validation
        all_inputs_valid, missing_fields = self.check.missing_input_check(
            user=self.user,
            userType=self.userType
        )
        if not all_inputs_valid:
            print(f"Error: The login {', '.join(missing_fields)} is missing, so the process will be rejected. Please re-try.")
            return
        
        # Validate account existence
        if not self.check.account_existence_check(self.user):
            print("Error: Invalid account holder name")
            return
        
        # Process login
        print("Login_Success")
        return self.return_transaction_output()
    
    def return_transaction_output(self):
        formatted_username = self.user.user_name.replace(" ", "_").ljust(21, "_")
        transaction_output = (
            f"01_{formatted_username}_"
            f"{self.user.account_number:>5}_"
            f"{self.userType}"
        )
        return transaction_output

if __name__ == "__main__":
    print("Welcome to the banking system")
    userType = input("Enter session type: ")
    user_name = input("Enter account holder name: ")
    account_number = input("Enter account number: ")
    
    user = type("User", (object,), {"user_name": user_name, "account_number": account_number, "userType": userType})
    login_instance = Login(userType, user)
    login_instance.process_login()
