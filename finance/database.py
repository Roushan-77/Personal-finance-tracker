import os
import sqlite3
import pandas as pd

# configuring the path of db file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = os.path.join(BASE_DIR, "..", "finance.db")


# connecting database
def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

#  creating database for safe if not exist , it will create and can be run multiple times
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            amount REAL,
            category TEXT,
            date TEXT,
            description TEXT,
            source TEXT,
            recurring INTEGER,
            payment_method TEXT,
            essential INTEGER
        )
    """)

    conn.commit()
    conn.close()


def insert_transaction(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
# inserting the data 
    cursor.execute("""
        INSERT INTO transactions (
            type, amount, category, date, description,
            source, recurring, payment_method, essential
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("type"),
        data.get("amount"),
        data.get("category"),
        data.get("date"),
        data.get("description"),
        data.get("source"),
        int(data.get("recurring", 0)),
        data.get("payment_method"),
        int(data.get("essential", 0))
    ))

    conn.commit()
    conn.close()


def get_monthly_summary_from_db(month: str):
    conn = get_connection()
    cursor = conn.cursor()

# summery for each month for better insight
    cursor.execute("""
        SELECT
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS total_income,
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS total_expense
        FROM transactions
        WHERE date LIKE ?
    """, (f"{month}%",))

    row = cursor.fetchone()
    conn.close()

    total_income = row[0] or 0
    total_expense = row[1] or 0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "savings": total_income - total_expense
    }


# using panads for better veiw in the form of DataFrame
def get_transactions_df(month: str = None):
    conn = get_connection()

    query = "SELECT * FROM transactions"
    params = ()

    if month:
        query += " WHERE date LIKE ?"
        params = (f"{month}%",)

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    return df