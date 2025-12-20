from finance.model import Income, Expense
from finance.database import insert_transaction, get_transactions_df, get_monthly_summary_from_db


class FinanceManager:
    def add_transaction(self, transaction):
        transaction.validate()
        data = transaction.to_dict()

# dynamiclly decides transaction type
        if isinstance(transaction, Income):
            data["type"] = "income"
        elif isinstance(transaction, Expense):
            data["type"] = "expense"
        else:
            raise ValueError("Unknown transaction type")

        insert_transaction(data)

# Delegate aggregation to SQL
    def get_monthly_summary(self, month: str):
        return get_monthly_summary_from_db(month)


# data fetch for DataFrame
    def get_transactions_table(self, month: str = None):
        df = get_transactions_df(month)

        if df.empty:
            return None

# droping internal id as not needed
        df = df.drop(columns=["id"], errors="ignore")


# making boolean to "Yes" and "No" for better readability
        if "recurring" in df.columns:
            df["recurring"] = df["recurring"].map({1: "Yes", 0: "No"})

        if "essential" in df.columns:
            df["essential"] = df["essential"].map({1: "Yes", 0: "No"})

        return df

