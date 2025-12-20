from datetime import datetime


# Base class containing common fields
class Transaction:
    def __init__(self, amount: float, category: str, date: str, description: str = None):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

#  a check before data being inserted to database
    def validate(self):
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        if not self.category:
            raise ValueError("Category is required")
        
        #  insuring the date foramt
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format (YYYY-MM-DD)")

#  converting objects to dict
    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }

# to get month, it slices the date to YY-MM
    def get_month(self):
        return self.date[:7]

    def __str__(self):
        return f"{self.category} - {self.amount} on {self.date}"


# income class drived from base class
class Income(Transaction):
    def __init__(self, amount: float, category: str, date: str, source: str, recurring: bool = False, description: str = None):
        super().__init__(amount, category, date, description)
        self.source = source
        self.recurring = recurring

# 1st runs the base validation
    def validate(self):
        super().validate()
        if not self.source:
            raise ValueError("Source is required")

# update the dict with new fields
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "source": self.source,
            "recurring": self.recurring
        })
        return data


# another class derived from base class
class Expense(Transaction):
    def __init__(self, amount: float, category: str, date: str, payment_method: str, essential: bool = False, description: str = None):
        super().__init__(amount, category, date, description)
        self.payment_method = payment_method
        self.essential = essential

    def validate(self):
        super().validate()
        if not self.payment_method:
            raise ValueError("Payment method is required")

# updates the dict
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "payment_method": self.payment_method,
            "essential": self.essential
        })
        return data
