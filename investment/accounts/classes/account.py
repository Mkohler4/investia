class Account:
    def __init__(self, name, balance, input_rate, grow_rate):
        """
        Initialize the Account.
        
        :param name: str - The name of the account.
        :param balance: float - The initial balance of the account.
        :param input_rate: float - The amount of money deposited per period.
        :param grow_rate: float - The growth rate per period (e.g., 0.01 for 1% growth per period).
        """
        self.name = name
        self.balance = balance
        self.input_rate = input_rate
        self.grow_rate = grow_rate

    def update_balance(self, time_periods):
        """
        Update the balance over a number of time periods.

        :param time_periods: int - The number of periods to apply the growth and deposits.
        """
        for _ in range(time_periods):
            # Add the deposited amount to the balance
            self.balance += self.input_rate
            # Apply the growth rate (compounding)
            self.balance *= (1 + self.grow_rate)

    def __str__(self):
        return f'{self.name}: {self.balance}'