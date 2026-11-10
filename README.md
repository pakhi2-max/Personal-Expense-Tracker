# PocketLedger — Personal Expense Tracker

A Flask-based full-stack web application to record income and expenses, organise transactions by category, review monthly summaries, visualise spending, and manage a monthly budget.

## Features

- Account signup, login and logout using Flask-Login.
- Password hashing using Werkzeug.
- User-specific transaction records.
- Create, view, edit and delete income/expense entries.
- Categories: Food, Travel, Bills, Shopping, Entertainment, Education, Healthcare, Salary, Freelance and Other.
- Filter transactions by type, category and date range.
- Monthly income, expenses and net balance.
- Category-wise expense doughnut chart using Chart.js.
- Monthly budget tracking and progress indicator.
- Export transactions to CSV.
- Responsive Bootstrap interface.
- CSRF protection for forms.

## Technology stack

- Python 3.10+
- Flask, Flask-Login, Flask-SQLAlchemy, Flask-WTF
- SQLite
- HTML, CSS, Bootstrap 5
- JavaScript and Chart.js

## Project structure

```text
personal_expense_tracker/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── models.py
│   ├── transactions.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── dashboard.html
│   │   ├── transactions.html
│   │   └── transaction_form.html
│   └── static/
│       └── css/style.css
├── instance/                 # SQLite database created automatically
├── config.py
├── run.py
├── requirements.txt
├── .env.example
└── README.md
```

## Run on Windows (VS Code)

1. Install Python 3.10 or newer and open this folder in VS Code.
2. Open Terminal → New Terminal.
3. Create a virtual environment:

   ```powershell
   python -m venv venv
   ```

4. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run `venv\Scripts\activate.bat`.

5. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Start the app:

   ```powershell
   python run.py
   ```

7. Open `http://127.0.0.1:5000` in your browser.
8. Create an account, log in, and add a few sample income and expense entries.

The SQLite database is created automatically at `instance/finance_tracker.db`.

## First-use test checklist

1. Sign up with a new username, email and password (at least 8 characters).
2. Add an income entry, such as Salary, and an expense entry, such as Food.
3. Confirm the dashboard totals and category chart update.
4. Edit one entry and confirm the new value appears.
5. Filter the transaction list by type, category and date.
6. Set a monthly budget and check the progress indicator.
7. Delete a test entry and export the remaining transactions as CSV.
8. Create a second account and verify it cannot see the first account's transactions.

## Deployment notes

This project is suitable as a starting point for Render or Railway. Before public deployment:

- Set a strong, random `SECRET_KEY` as an environment variable.
- Set `debug=False` and use a production WSGI server such as Gunicorn.
- Use the included `Procfile` and `wsgi.py` as the Gunicorn entry point on supported Linux hosts.
- Use managed PostgreSQL for a multi-instance deployment; local SQLite files may not persist across ephemeral deployments.
- Configure HTTPS and review hosting platform environment-variable and persistent-storage settings.
- Do not commit `.env`, database files, or real financial records to GitHub.

## Limitations

- The app does not connect to banks or payment services.
- Currency is displayed as INR (₹) in the interface.
- Chart.js and Bootstrap are loaded from public CDNs, so those assets require internet access.
- This is an educational project, not regulated accounting or financial advice software.
