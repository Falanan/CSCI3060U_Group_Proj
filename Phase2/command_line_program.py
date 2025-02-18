def banking_system():
    logged_in = False
    accounts = {
        "Xuan_Zheng": {"00003": 1200.0},
    }
    
    while True:
        command = input()
        if command == "login":
            print("Welcome to the banking system")
            
            if logged_in:
                print("You have already Login")
                continue
            
            print("Enter session type:", end=" ")
            session_type = input()
            print(f"Enter session type: {session_type}")
            
            if session_type == "admin":
                print("Login_Success")
                logged_in = True
                print("Enter account holder name:", end=" ")
                account_holder = input()
                print(f"Enter account holder name: {account_holder}")
                
                if account_holder not in accounts:
                    print("Error: Invalid account holder name")
                    continue
                
                print("Enter account name:", end=" ")
                account_number = input()
                print(f"Enter account name: {account_number}")
                
                if account_number not in accounts[account_holder]:
                    print("Error: Invalid account number")
                    continue
                
                print("Enter Withdrawal amount:", end=" ")
                amount = float(input())
                print(f"Enter Withdrawal amount: {amount}")
                
                if accounts[account_holder][account_number] < amount:
                    print("Error: Account balance less than 0")
                else:
                    accounts[account_holder][account_number] -= amount
                    print("Withdrawal success")
            
            elif session_type == "standard":
                print("Enter account holder name:", end=" ")
                account_holder = input()
                print(f"Enter account holder name: {account_holder}")
                
                if account_holder not in accounts:
                    print("Error: Invalid account holder name")
                    continue
                
                print("Enter account name:", end=" ")
                account_number = input()
                print(f"Enter account name: {account_number}")
                
                if account_number not in accounts[account_holder]:
                    print("Error: Wrong account number")
                    continue
                
                print("Enter Withdrawal amount:", end=" ")
                amount = float(input())
                print(f"Enter Withdrawal amount: {amount}")
                
                if accounts[account_holder][account_number] < amount:
                    print("Error: Account balance less than 0")
                else:
                    accounts[account_holder][account_number] -= amount
                    print("Withdrawal success")
            
        else:
            print("Invalid command")

if __name__ == "__main__":
    banking_system()
