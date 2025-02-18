class Check:
    def user_check(self, user1, user2):
        return user1.account_number != user2.account_number

    def availability_check(self, user):
        return user.availability == "A"

    def balance_check(self, user, amount):
        return user.balance >= amount

    def limit_check(self, amount, limit):
        return amount <= limit

    def negative_amount_check(self, amount):
        return amount > 0

    def zero_amount_check(self, amount):
        return amount != 0

    def account_existence_check(self, user):
        return user is not None

    def admin_override_check(self, user):
        return user.userType == "admin"

    def valid_company_check(self, company):
        VALID_COMPANIES = ["EC", "CQ", "FI"]
        return company in VALID_COMPANIES

    def company_id_check(self, company):
        COMPANY_ACCOUNTS = {
            "EC": "10000",
            "CQ": "20000",
            "FI": "30000"
        }
        return COMPANY_ACCOUNTS.get(company)

    def invalid_character_check(self, value):
        try:
            float(value)
            return True
        # except ValueError:
        except(ValueError, TypeError):
            return False

    def missing_input_check(self, **kwargs):
        missing_fields = [key for key, value in kwargs.items() if not value]

        if missing_fields:
            return False, missing_fields
        return True, ""
    
    def sender_account_match(self, user, sender_account):
        """
        Check if the sender account number matches the logged-in user's account.
        """
        return user.account_number == sender_account
