from datetime import date
from objects.items.object import BaseObject

class Mortgage(BaseObject):
    def __init__(self, price, annual_interest_rate, term_years, down_payment_percentage=None, date=date.today()):
        super().__init__(price, date)
        self.annual_interest_rate = annual_interest_rate
        self.term_years = term_years
        self.down_payment_percentage = down_payment_percentage
        self.monthly_interest_rate = self.annual_interest_rate / 12 / 100
        self.total_payments = self.term_years * 12
        self.down_payment = self.calculate_down_payment()

    def calculate_down_payment(self):
        if self.price < 500000:
            down_payment = self.price * 0.05
        elif self.price < 1000000:
            down_payment = 500000 * 0.05 + (self.price - 500000) * 0.10
        else:
            down_payment = self.price * 0.20
        
        if self.down_payment_percentage is not None:
            required_down_payment = self.price * (self.down_payment_percentage / 100)
            if required_down_payment < down_payment:
                raise ValueError(f"Down payment must be at least ${down_payment:.2f} for a house priced at ${self.price}.")
            return required_down_payment

        return down_payment

    def calculate_monthly_payment(self):
        r = self.monthly_interest_rate
        n = self.total_payments
        P = self.price - self.down_payment

        monthly_payment = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
        return monthly_payment
    
    def recalculate_for_remaining_term(self, remaining_principal, remaining_years):
        r = self.monthly_interest_rate
        n = remaining_years * 12
        P = remaining_principal

        monthly_payment = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
        return monthly_payment
    
    def update_date(self, new_date):
        self.date = new_date

class House(Mortgage):
    def __init__(self, price, annual_interest_rate, term_years, down_payment_percentage=None, min_price=0, max_price=1000000):
        super().__init__(price, annual_interest_rate, term_years, down_payment_percentage)
        self.min_price = min_price
        self.max_price = max_price

    

    
## EXAMPLE USAGE
# house_price = 800000
# annual_interest_rate = 5
# term_years = 30
# down_payment_percentage = None  # or a specific percentage like 10

# calculator = MortgageCalculator(house_price, annual_interest_rate, term_years, down_payment_percentage)
# initial_monthly_payment = calculator.calculate_monthly_payment()
# print(f"Initial Monthly Payment: ${initial_monthly_payment:.2f}")

# # Assume 15 years have passed and the remaining principal is $450,000
# remaining_principal = 450000
# remaining_years = 15
# remaining_monthly_payment = calculator.recalculate_for_remaining_term(remaining_principal, remaining_years)
# print(f"Remaining Monthly Payment: ${remaining_monthly_payment:.2f}")