@echo off
echo Starting Expense Management System...

REM OPTIONAL: Activate virtual environment if you have one
REM call .venv\Scripts\activate

REM Install required packages (if needed)
echo Installing requirements...
pip install -r requirements.txt

REM Start backend
start cmd /k "cd backend && uvicorn server:app --reload"

REM Wait a little to ensure backend starts before frontend
timeout /t 3 >nul

REM Start frontend
start cmd /k "cd frontend && streamlit run app.py"

exit
