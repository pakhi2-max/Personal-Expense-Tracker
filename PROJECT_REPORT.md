# Project Report: PocketLedger — Personal Expense Tracker Web App

## 1. Introduction
PocketLedger is a Python-based web application designed to help individuals record and review their day-to-day finances. Users can add income and expense transactions, assign categories, view a monthly overview, and compare spending with a monthly budget. The application combines a Flask backend, SQLite database, and responsive browser interface.

## 2. Aim
To develop a full-stack web application that demonstrates user authentication, database-backed CRUD operations, transaction categorisation, and visual financial summaries.

## 3. Objectives
- Provide signup, login and logout functionality.
- Store each user's transactions separately.
- Support adding, viewing, editing and deleting transactions.
- Categorise income and expenses.
- Filter transactions by type, category and date range.
- Calculate monthly income, expenses and net balance.
- Display category-wise expense analytics.
- Allow a monthly spending budget and CSV export.

## 4. Technology Used
| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Web framework and routing |
| Flask-Login | Session-based authentication |
| Flask-SQLAlchemy | ORM and database operations |
| SQLite | Local relational database |
| Werkzeug | Password hashing |
| Flask-WTF | CSRF protection |
| HTML/CSS/Bootstrap | Responsive user interface |
| JavaScript/Chart.js | Expense chart |

## 5. System Design
The browser sends requests to Flask routes. Authentication routes validate user credentials. Transaction routes validate form data and use SQLAlchemy to read or modify SQLite records. Every transaction query is restricted to the currently logged-in user's ID. The dashboard aggregates the selected month's income and expenses and sends category totals to Chart.js.

### Main database entities
**User:** id, username, email, password_hash, created_at.

**Transaction:** id, user_id, kind, amount, category, description, transaction_date, created_at.

**Budget:** id, user_id, month, amount.

A user can own multiple transactions and monthly budgets. Foreign keys connect each record to its owner.

## 6. Functional Modules
1. **Authentication:** account creation, login and logout.
2. **Transaction management:** add, list, edit and delete income/expense entries.
3. **Categorisation and filtering:** categories plus type and date filters.
4. **Dashboard:** monthly income, expenses, net balance and recent activity.
5. **Analytics:** category-wise expense doughnut chart.
6. **Budget management:** save a monthly target and compare actual spending.
7. **Export:** download transaction records as CSV.

## 7. Validation and Security
Passwords are stored as hashes, not plain text. Forms use CSRF tokens. Amounts must be positive, transaction types and categories are validated, and database queries for transaction operations include the current user's ID. For deployment, a unique secret key, HTTPS, production server and persistent database storage must be configured.

## 8. How to Execute
Install Python 3.10+, create and activate a virtual environment, install packages using `pip install -r requirements.txt`, then run `python run.py`. Open `http://127.0.0.1:5000`, create an account and begin entering sample transactions. Full Windows commands are provided in README.md.

## 9. Testing Plan
- Verify account registration and duplicate-account validation.
- Verify successful and unsuccessful login.
- Add income and expense records and verify totals.
- Edit and delete a transaction.
- Check category and date filters.
- Check monthly budget progress.
- Export CSV and inspect its columns.
- Verify that one account cannot access another account's records.

## 10. Expected Outcome
The completed application provides a simple interface for maintaining personal income and expense records. It helps users understand monthly cash flow and category-level spending through summaries and a chart. Actual results should be recorded after running the test checklist; no test results are assumed in this report.

## 11. Future Scope
- Receipt image upload and OCR.
- Recurring transactions.
- More detailed date-range and year-over-year analytics.
- Downloadable PDF reports.
- Optional multi-currency support.
- Automated tests and deployment pipeline.

## 12. Conclusion
PocketLedger demonstrates how Python and Flask can be used to build a practical full-stack application. It combines authentication, relational data storage, CRUD functionality and visual analytics in one responsive web interface.
