from django.db import router
from fastapi import APIRouter, HTTPException
from models import UserSignup, UserLogin, OTPVerify
from auth_helper import hash_password, verify_password, generate_otp, send_otp, otp_store
from db_helper import get_db_cursor  # ✅ Use shared DB helper


router = APIRouter()

@router.post("/signup")
def signup(user: UserSignup):
    with get_db_cursor() as cursor:  # 🔥 Remove `commit=False`
        cursor.execute("SELECT id FROM users WHERE email=%s", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="User already exists.")

    otp = generate_otp()
    otp_store[user.email] = {
        "otp": otp,
        "password": hash_password(user.password)
    }

    send_otp(user.email, otp)  # or False for real email
    print(f"✅ OTP {otp} sent to {user.email}")
    return {"message": "OTP sent for verification."}




@router.post("/verify")
def verify_otp(data: OTPVerify):
    try:
        entry = otp_store.get(data.email)
        if entry and entry["otp"] == data.otp:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                    (data.email, entry["password"])
                )
            otp_store.pop(data.email)
            print(f"✅ User {data.email} registered successfully.")
            return {"message": "Signup successful."}
        raise HTTPException(status_code=400, detail="Invalid OTP")

    except Exception as e:
        print("❌ Verification Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/login")
def login(user: UserLogin):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id, password_hash FROM users WHERE email = %s", (user.email,))
        row = cursor.fetchone()

        if row and verify_password(user.password, row["password_hash"]):
            return {"message": "Login successful", "user_id": row["id"]}

        raise HTTPException(status_code=401, detail="Invalid email or password")


@router.get("/user_id/{email}")
async def get_user_id(email: str):
    try:
        print(f"🔍 Starting user_id lookup for: {email}")
        with get_db_cursor() as cursor:
            print("✅ DB connection established")
            cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
            print("✅ Query executed")
            result = cursor.fetchone()
            print(f"✅ Query result: {result}")
            
            if result:
                return {"user_id": result["id"]}
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print(f"❌ Error in get_user_id: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

