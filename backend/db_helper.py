from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv

from logging_setup import setup_logger

logger = setup_logger('db_helper')
load_dotenv()

@contextmanager
def get_db_cursor(commit=False):
    env = os.getenv("ENV")

    if env == "DEV":
        print("Dev inside")
        db_config = {
            "host": os.getenv("DEV_DB_HOST"),
            "user": os.getenv("DEV_DB_USER"),
            "password": os.getenv("DEV_DB_PASSWORD"),
            "database": os.getenv("DEV_DB_NAME")
        }

    elif env == "PROD":
        print("Prod inside")
        db_config = {
            "host": os.getenv("PROD_DB_HOST"),
            "user": os.getenv("PROD_DB_USER"),
            "password": os.getenv("PROD_DB_PASSWORD"),
            "database": os.getenv("PROD_DB_NAME")
        }

    # ✅ FIX: Define the connection here

    connection = mysql.connector.connect(**db_config)

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

def fetch_expenses_for_date(user_id, expense_date):
    logger.info(f"Fetching expenses for user {user_id} on {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT amount, category, notes FROM expenses WHERE user_id = %s AND expense_date = %s",
            (user_id, expense_date)
        )
        return cursor.fetchall()


def delete_expenses_for_date(user_id, expense_date):
    logger.info(f"Deleting expenses for user {user_id} on {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "DELETE FROM expenses WHERE user_id = %s AND expense_date = %s",
            (user_id, expense_date)
        )


def insert_expense(user_id, expense_date, amount, category, notes):
    logger.info(f"Inserting expense for user {user_id} on {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (user_id, expense_date, amount, category, notes) VALUES (%s, %s, %s, %s, %s)",
            (user_id, expense_date, amount, category, notes)
        )


def fetch_expense_summary(user_id, start_date, end_date):
    logger.info(f"Summary from {start_date} to {end_date} for user {user_id}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''
            SELECT category, SUM(amount) as total 
            FROM expenses 
            WHERE user_id = %s AND expense_date BETWEEN %s AND %s  
            GROUP BY category;
            ''',
            (user_id, start_date, end_date)
        )
        return cursor.fetchall()


def fetch_monthly_expense_summary(user_id):
    logger.info(f"Monthly summary for user {user_id}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''
            SELECT DATE_FORMAT(expense_date, '%Y-%m') AS month, SUM(amount) AS total
            FROM expenses
            WHERE user_id = %s
            GROUP BY month
            ORDER BY month ASC;
            ''',
            (user_id,)
        )
        return cursor.fetchall()
from db_helper import get_db_cursor

def test_db_connection():
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            print("✅ Database connected successfully:", result)
    except Exception as e:
        print("❌ Failed to connect to the database:", str(e))




import os
if __name__ == "__main__":
    test_db_connection()

    insert_expense(1, "2025-04-18", 99.99, "Shopping", "Test insert from backend")
    expenses = fetch_expenses_for_date(1, "2025-04-18")
    print("Fetched expenses:", expenses)

    delete_expenses_for_date(1, "2025-04-18")
    print("Deleted today's expenses.")
    # expenses = fetch_expenses_for_date("2024-09-30")
    # print(expenses)
    # monthly_exp = fetch_monthly_expense_summary()
    # print(monthly_exp)
    # # delete_expenses_for_date("2024-08-25")
    # summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    # for record in summary:
    #     print(record)


