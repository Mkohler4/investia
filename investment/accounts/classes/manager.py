from datetime import date
from objects.items.house import House
from copy import deepcopy
import matplotlib.pyplot as plt
import streamlit as st

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
    
    def calculate_balance_over_time(self, months):
        # Prepare dictionary to hold balance projections for each account
        balances_over_time = {account.name: [account.balance] for account in self.accounts}

        # Calculate the monthly balance projections for all accounts
        for _ in range(months):
            for account in self.accounts:
                monthly_interest_rate = (1 + account.interest_rate / 100) ** (1/12) - 1
                current_balance = balances_over_time[account.name][-1]
                current_balance += account.input_rate
                current_balance *= (1 + monthly_interest_rate)
                balances_over_time[account.name].append(current_balance)

        # Calculate total balance over time
        total_balances = [sum(balances) for balances in zip(*balances_over_time.values())]
        
        return balances_over_time, total_balances
    
    def plot_projected_balances(self, months):
        account_balances, total_balances = self.calculate_balance_over_time(months)

        # Plotting the balances over time
        plt.figure(figsize=(12, 7))

        # Plot individual account balances
        for account_name, balances in account_balances.items():
            plt.plot(range(months + 1), balances, label=account_name)

        # Plot total balance
        plt.plot(range(months + 1), total_balances, label="Total Balance", linewidth=2, linestyle='--')

        plt.xlabel("Month")
        plt.ylabel("Balance ($)")
        plt.legend()
        plt.grid(True)

        # Use Streamlit to display the plot
        st.pyplot(plt)
    
    def calculate_total_income(self, months):
        # Calculate the projected total income over a number of months
        total_income = 0
        for account in self.accounts:
            balance = account.balance
            monthly_interest_rate = (1 + account.interest_rate / 100) ** (1/12) - 1
            for _ in range(months):
                balance += account.input_rate
                balance *= (1 + monthly_interest_rate)
            total_income += balance
        return total_income
    
    def calculate_account_groth(self, date, account):
        today = date.today()
        months_until_target = self.months_between(today, date)
        monthly_interest_rate = (1 + account.interest_rate / 100) ** (1/12) - 1
        balance = account.balance
        for _ in range(months_until_target):
            balance *= (1 + monthly_interest_rate)  # Apply monthly interest
            balance += account.input_rate  # Add monthly input rate
        return balance
    
    def calculate_income_at_date(self, target_object):
        # Create a copy of the accounts to avoid modifying the original
        accounts_copy = deepcopy(self.accounts)
        # Sort the list of objects based on the date attribute
        sorted_objects = sorted(self.objects, key=lambda obj: obj.date)
        # Sort accounts by interest rate from lowest to highest and then by balance
        sorted_accounts = sorted(accounts_copy, key=lambda account: (account.interest_rate, account.balance))

        # Iterate over the sorted objects to process each purchase in order
        for obj in sorted_objects:
            # Stop processing if the object's date is after the target object's date
            if obj.date >= target_object.date:
                break

            today = date.today()
            months_until_target = self.months_between(today, target_object.date)

            # Update each account's balance for the months between current_date and obj.date
            for account in sorted_accounts:
                monthly_interest_rate = (1 + account.interest_rate / 100) ** (1/12) - 1
                for _ in range(months_until_target):
                    account.balance *= (1 + monthly_interest_rate)  # Apply monthly interest
                    account.balance += account.input_rate  # Add monthly input rate

            # Start with the object's price
            remaining_price = obj.price

            # Iterate over sorted accounts to deduct the price
            for account in sorted_accounts:
                if account.balance >= remaining_price:
                    # Deduct the entire remaining price from this account
                    account.balance -= remaining_price
                    remaining_price = 0
                    break  # Object fully paid for, exit the loop
                else:
                    # Deduct as much as possible from this account
                    remaining_price -= account.balance
                    account.balance = 0

            # Check if the object was successfully purchased
            if remaining_price > 0:
                print(f"Not enough funds to purchase '{obj.name}'.")
            else:
                print(f"Object '{obj.name}' purchased successfully.")

            # Stop the process if the target object is reached
            if obj == target_object:
                break

        # Calculate the total income (remaining balance) across all copied accounts
        total_income = sum(account.balance for account in sorted_accounts)
        return total_income

    def calculate_affordability(self, target_object):
        today = date.today()
        months_until_target = self.months_between(today, target_object.date)

        # Calculate total_income until the target object's date
        total_income = self.calculate_total_income(months_until_target)

        net_affordability = 0
        # If the target object is a House, subtract the down payment
        if isinstance(target_object, House):
            down_payment = target_object.calculate_down_payment()
            net_affordability = total_income - down_payment
        else:
            # Calculate net affordability for target object
            net_affordability = total_income - target_object.price

        print(f"Net affordability for target object: ${net_affordability:.2f}")

        # Adjust other objects if needed
        self.adjust_other_objects(target_object, net_affordability)

        return net_affordability

    def adjust_other_objects(self, target_object, net_affordability):
        """Adjusts other objects' attributes to ensure overall affordability."""
        print("Adjusting other objects...")

        # Sort objects by purchase date
        sorted_objects = sorted(self.objects, key=lambda obj: obj.date)
        
        # Find the index of the target object
        target_index = sorted_objects.index(target_object)

        # Iterate through objects in chronological order
        for idx, obj in enumerate(sorted_objects):
            if idx != target_index:
                # Calculate months between the target object's date and the next purchase
                months_after_target = self.months_between(target_object.date, obj.date)

                print(f"Months after target: {months_after_target}")

                # Update income growth between the target object and this object
                additional_income = self.calculate_income_at_date(target_object)
                remaining_net_affordability += additional_income

                print(f"Remaining net affordability: ${remaining_net_affordability:.2f}")

                if isinstance(target_object, House) and target_index < idx:
                    # Subtract monthly mortgage payments if purchasing objects after the house
                    monthly_payment = target_object.calculate_monthly_payment()
                    remaining_net_affordability -= monthly_payment * months_after_target

                    print(f"Remaining net affordability after mortgage payments: ${remaining_net_affordability:.2f}")

                if isinstance(obj, House):
                    down_payment = obj.calculate_down_payment()
                    print(f"Down payment for House {idx + 1}: ${down_payment:.2f}")
                    if remaining_net_affordability - down_payment < 0:
                        reduction = min(obj.price, abs(remaining_net_affordability))
                        obj.price -= reduction
                        remaining_net_affordability += reduction
                        print(f"Adjusted House price to: ${obj.price:.2f}")
                else:
                    if remaining_net_affordability + obj.price < 0:
                        reduction = min(obj.price, abs(remaining_net_affordability))
                        obj.price -= reduction
                        remaining_net_affordability += reduction
                        print(f"Adjusted Object price to: ${obj.price:.2f}")

    

    