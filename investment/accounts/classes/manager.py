from datetime import date
from objects.items.house import House

class FinancialManager:
    def __init__(self):
        self.accounts = []
        self.saving_goals = []
        self.monthly_expenses = []
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def add_account(self, account):
        self.accounts.append(account)

    def add_savings_goal(self, goal):
        self.saving_goals.append(goal)
    
    def add_monthly_expense(self, expense):
        self.monthly_expenses.append(expense)
    
    def update_savings_goal(self, name, target_amount=None, target_date=None):
        for goal in self.saving_goals:
            if goal.name == name:
                if target_amount is not None:
                    goal.target_amount = target_amount
                if target_date is not None:
                    goal.target_date = target_date

    def months_between(self, start_date, end_date):
        """
        Calculate the number of months between two dates.
        """
        return (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

    def calculate_affordability(self, target_date, target_object):
        today = date.today()
        months = self.months_between(today, target_date)

        # Calculate total_income
        total_income = 0
        for account in self.accounts:
            balance = account.balance
            monthly_interest_rate = (1 + account.interest_rate / 100) ** (1/12) - 1
            for _ in range(months):
                balance += account.input_rate
                balance *= (1 + monthly_interest_rate)
            total_income += balance

        # Calculate total expenses
        total_expenses = sum([expense.amount for expense in self.monthly_expenses]) * months

        # Check if the target object is a House
        if isinstance(target_object, House):
            down_payment = target_object.calculate_down_payment()
            if total_income < down_payment:
                print(f"Cannot afford the down payment of ${down_payment:.2f} by {target_date}")
                return total_income - total_expenses

            # Adjust total income after down payment
            total_income -= down_payment

            # Calculate mortgage affordability
            monthly_mortgage_payment = target_object.calculate_monthly_payment()
            remaining_months = target_object.term_years * 12 - months
            mortgage_expenses = monthly_mortgage_payment * remaining_months

            if total_income < mortgage_expenses:
                print(f"Cannot afford the mortgage payments of ${monthly_mortgage_payment:.2f} per month after the down payment.")
                return total_income - total_expenses

            print(f"Can afford the down payment and mortgage payments for the house by {target_date}")
            return total_income - total_expenses

        # If the target object is not a House, just print the net affordability
        net_affordability = total_income - total_expenses
        print(f"Net affordability: ${net_affordability:.2f}")

        return net_affordability

    

    