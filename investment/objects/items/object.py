from datetime import date

class BaseObject:
    def __init__(self, price, date=date.today()):
        self.price = price
        self.date = date