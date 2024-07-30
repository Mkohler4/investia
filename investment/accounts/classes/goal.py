class Goal:
    def __init__(self, target_date, target_amount=0, saved_amount=0):
        self.target_amount = target_amount
        self.target_date = target_date
        self.saved_amount = saved_amount

    def __str__(self):
        return f"{self.name} - {self.amount} - {self.due_date}"