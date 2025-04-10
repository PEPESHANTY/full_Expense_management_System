import os
import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger
from dotenv import load_dotenv

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
            "database": os.getenv("DEV_DB_NAME"),
            "port": os.getenv("DEV_DB_PORT"),
        }

    elif env == "PROD":
        print("Prod inside")
        db_config = {
            "host": os.getenv("PROD_DB_HOST"),
            "user": os.getenv("PROD_DB_USER"),
            "password": os.getenv("PROD_DB_PASSWORD"),
            "database": os.getenv("PROD_DB_NAME"),
            "port": os.getenv("PROD_DB_PORT"),
        }

    # ✅ FIX: Define the connection here

    connection = mysql.connector.connect(**db_config)

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date
               BETWEEN %s and %s  
               GROUP BY category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

def fetch_monthly_expense_summary():
    logger.info("fetch_monthly_expense_summary called")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''
            SELECT DATE_FORMAT(expense_date, '%Y-%m') AS month,SUM(amount) AS total
            FROM expenses
            GROUP BY month
            ORDER BY month ASC;
            '''
        )
        data = cursor.fetchall()
        return data


import os
if __name__ == "__main__":


    expenses = fetch_expenses_for_date("2024-09-30")
    print(expenses)
    monthly_exp = fetch_monthly_expense_summary()
    print(monthly_exp)
    # delete_expenses_for_date("2024-08-25")
    summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    for record in summary:
        print(record)
