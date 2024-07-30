class FinancialManager:
    def __init__(self):
        self.accounts = []
        self.saving_goals = []
        self.monthly_expenses = []

    def add_account(self, account):
        self.accounts.append(account)

    def add_savings_goal(self, goal):
        self.saving_goals.append(goal)
    
    def update_savings_goal(self, name, target_amount=None, target_date=None):
        for goal in self.saving_goals:
            if goal.name == name:
                if target_amount is not None:
                    goal.target_amount = target_amount
                if target_date is not None:
                    goal.target_date = target_date

    def contribute_to_savings(self, contribution_amount):
        for goal in self.saving_goals:
            for account in self.accounts:
                if account.balance >= contribution_amount:
                    account.balance -= contribution_amount
                    goal.saved_amount += contribution_amount
                    break

    def add_monthly_expense(self, expense):
        self.monthly_expenses.append(expense)

    

    