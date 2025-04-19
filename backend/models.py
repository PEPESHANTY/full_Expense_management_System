# backend/models.py
from pydantic import BaseModel, EmailStr


class ExpenseCreate(BaseModel):
    user_id: int
    expense_date: str  # Format: YYYY-MM-DD
    amount: float
    category: str
    notes: str

class UserSignup(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str
