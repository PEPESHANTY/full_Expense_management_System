
# auth_helper.py

import hashlib
import random
import smtplib
from email.message import EmailMessage
import os
from http.client import HTTPException
from models import UserSignup
from dotenv import load_dotenv
from contextlib import contextmanager
import mysql.connector


load_dotenv()
otp_store = {}

# 🔐 Password handling
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(input_password: str, stored_hash: str) -> bool:
    return hash_password(input_password) == stored_hash

# 🔢 OTP generation
def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(email: str, otp: str, dry_run: bool = False):
    if dry_run:
        print(f"[DRY RUN] OTP for {email} would be: {otp}")
        return

    msg = EmailMessage()
    msg.set_content(f"Your OTP is {otp}.Please use this OTP to verify your account.")
    msg["Subject"] = "Expense App OTP Verification"
    msg["From"] = os.getenv("EMAIL_SENDER")
    msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASS"))
        smtp.send_message(msg)

# 🧠 Simple DB cursor wrapper
@contextmanager
def get_db_cursor():
    env = os.getenv("ENV", "DEV")

    if env == "PROD":
        db_config = {
            "host": os.getenv("PROD_DB_HOST"),
            "user": os.getenv("PROD_DB_USER"),
            "password": os.getenv("PROD_DB_PASSWORD"),
            "database": os.getenv("PROD_DB_NAME"),
            "port": int(os.getenv("PROD_DB_PORT", 3306))
        }
    else:
        db_config = {
            "host": os.getenv("DEV_DB_HOST"),
            "user": os.getenv("DEV_DB_USER"),
            "password": os.getenv("DEV_DB_PASSWORD"),
            "database": os.getenv("DEV_DB_NAME"),
            "port": int(os.getenv("DEV_DB_PORT", 3306))
        }


    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()


# ✅ Manual testing
# if __name__ == "__main__":
    # test_email = "shantanubhute3@gmail.com"
    # otp = generate_otp()
    # otp_store[test_email] = {"otp": otp, "password": hash_password("Shanty@18")}
    # print(f"🚀 Generated OTP: {otp}")
    # send_otp(test_email, otp, dry_run=True)  # Toggle dry_run to True for testing only
    # print("✅ Email sent. Check your inbox/spam.")
    #
    # from models import UserSignup
    #
    # test_user = UserSignup(email="shantanubhute3@example.com", password="Shanty@18")
    # try:
    #     result = signup_logic(test_user)
    #     print("✅ Signup Test Passed:", result)
    # except Exception as e:
    #     print("❌ Signup Test Failed:", str(e))






# # backend/auth_helper.py
# import hashlib
# import random
# import smtplib
# import mysql.connector
# from email.message import EmailMessage
# from contextlib import contextmanager
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
# otp_store = {}
#
# # ✅ Password hashing
# def hash_password(password: str) -> str:
#     return hashlib.sha256(password.encode()).hexdigest()
#
# def verify_password(input_password: str, stored_hash: str) -> bool:
#     return hash_password(input_password) == stored_hash
#
# # ✅ OTP logic
# def generate_otp():
#     return str(random.randint(100000, 999999))
#
# def send_otp(email: str, otp: str):
#     msg = EmailMessage()
#     msg.set_content(f"Your OTP is {otp}. Please use this OTP to verify your account.")
#     msg["Subject"] = "Expense App OTP Verification"
#     msg["From"] = os.getenv("EMAIL_SENDER")
#     msg["To"] = email
#
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#         smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASS"))
#         smtp.send_message(msg)
#
# # ✅ DB Connection logic copied from db_helper.py
# @contextmanager
# def get_db_cursor(commit=False):
#     env = os.getenv("ENV")
#
#     db_config = {
#         "host": os.getenv(f"{env}_DB_HOST"),
#         "user": os.getenv(f"{env}_DB_USER"),
#         "password": os.getenv(f"{env}_DB_PASSWORD"),
#         "database": os.getenv(f"{env}_DB_NAME")
#     }
#
#     connection = mysql.connector.connect(**db_config)
#     cursor = connection.cursor(dictionary=True)
#
#     try:
#         yield cursor
#         if commit:
#             connection.commit()
#     finally:
#         cursor.close()
#         connection.close()
#
# if __name__ == "__main__":
#     with get_db_cursor() as cursor:
#         cursor.execute("SELECT 1;")
#         print("✅ DB Connected:", cursor.fetchone())
#
#     test_email = "shantanubhute3@gmail.com"  # Replace with your real or temp email
#     otp = generate_otp()
#     print(f"📨 Sending OTP: {otp} to {test_email}")
#     send_otp(test_email, otp)
#     print("✅ Email sent! Check your inbox.")

