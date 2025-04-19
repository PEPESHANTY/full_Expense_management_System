from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
from pydantic import BaseModel

import db_helper
from auth_routes import router as auth_router

app = FastAPI()
app.include_router(auth_router)

# 📦 Models
class Expense(BaseModel):
    #expense_date: str
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

@app.get("/")
def root():
    return {"message": "Backend is running successfully!"}

# ✅ POST: Add or update expenses for a specific user
@app.post("/expenses/{user_id}/{expense_date}")
def add_or_update_expense(user_id: int, expense_date: date, expenses: List[Expense]):
    print("Incoming data:", expenses)
    db_helper.delete_expenses_for_date(user_id, str(expense_date))
    for expense in expenses:
        db_helper.insert_expense(
            user_id,
            str(expense_date),
            expense.amount,
            expense.category,
            expense.notes
        )
    return {"message": "✅ Expenses updated successfully."}

# ✅ GET: Fetch expenses for a specific user on a given date
@app.get("/expenses/{user_id}/{expense_date}", response_model=List[Expense])
def get_expenses(user_id: int, expense_date: date):
    return db_helper.fetch_expenses_for_date(user_id, str(expense_date))

# ✅ POST: Get analytics between date range for a specific user
@app.post("/analytics/{user_id}")
def get_analytics(user_id: int, date_range: DateRange):
    data = db_helper.fetch_expense_summary(user_id, date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary")

    total = sum(row["total"] for row in data)
    breakdown = {
        row["category"]: {
            "total": row["total"],
            "percentage": (row["total"] / total * 100) if total else 0
        }
        for row in data
    }
    return breakdown

# ✅ GET: Monthly summary for a specific user
@app.get("/analytics_by_month/{user_id}")
def get_monthly_analytics(user_id: int):
    return db_helper.fetch_monthly_expense_summary(user_id)
