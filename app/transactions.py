import csv
from io import StringIO
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required, current_user
from sqlalchemy import func
from app import db
from app.models import Transaction, Budget

transactions_bp = Blueprint("transactions", __name__)
CATEGORIES = ["Food", "Travel", "Bills", "Shopping", "Entertainment",
              "Education", "Healthcare", "Salary", "Freelance", "Other"]

def parse_transaction_form():
    kind = request.form.get("kind", "")
    category = request.form.get("category", "")
    description = request.form.get("description", "").strip()
    try:
        amount = Decimal(request.form.get("amount", "0"))
        tx_date = datetime.strptime(request.form.get("transaction_date", ""), "%Y-%m-%d").date()
    except (InvalidOperation, ValueError):
        raise ValueError("Enter a valid amount and date.")
    if kind not in ("income", "expense"):
        raise ValueError("Choose income or expense.")
    if category not in CATEGORIES:
        raise ValueError("Choose a valid category.")
    if amount <= 0 or amount > Decimal("9999999999"):
        raise ValueError("Amount must be greater than zero.")
    return kind, amount, category, description, tx_date

@transactions_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("transactions.dashboard"))
    return redirect(url_for("auth.login"))

@transactions_bp.route("/dashboard")
@login_required
def dashboard():
    today = date.today()
    month = request.args.get("month", today.strftime("%Y-%m"))
    try:
        month_start = datetime.strptime(month, "%Y-%m").date().replace(day=1)
    except ValueError:
        month = today.strftime("%Y-%m")
        month_start = today.replace(day=1)
    if month_start.month == 12:
        next_month = month_start.replace(year=month_start.year + 1, month=1)
    else:
        next_month = month_start.replace(month=month_start.month + 1)

    query = Transaction.query.filter_by(user_id=current_user.id).filter(
        Transaction.transaction_date >= month_start,
        Transaction.transaction_date < next_month
    )
    monthly = query.all()
    income = sum((t.amount for t in monthly if t.kind == "income"), Decimal("0"))
    expenses = sum((t.amount for t in monthly if t.kind == "expense"), Decimal("0"))
    category_totals = {}
    for tx in monthly:
        if tx.kind == "expense":
            category_totals[tx.category] = category_totals.get(tx.category, Decimal("0")) + tx.amount

    budget = Budget.query.filter_by(user_id=current_user.id, month=month).first()
    recent = Transaction.query.filter_by(user_id=current_user.id).order_by(
        Transaction.transaction_date.desc(), Transaction.id.desc()
    ).limit(8).all()
    return render_template("dashboard.html", month=month, income=income, expenses=expenses,
                           balance=income-expenses, category_labels=list(category_totals.keys()),
                           category_values=[float(v) for v in category_totals.values()],
                           recent=recent, budget=budget, budget_used=expenses)

@transactions_bp.route("/transactions")
@login_required
def list_transactions():
    query = Transaction.query.filter_by(user_id=current_user.id)
    kind = request.args.get("kind", "")
    category = request.args.get("category", "")
    start = request.args.get("start", "")
    end = request.args.get("end", "")
    if kind in ("income", "expense"):
        query = query.filter_by(kind=kind)
    if category in CATEGORIES:
        query = query.filter_by(category=category)
    try:
        if start:
            query = query.filter(Transaction.transaction_date >= datetime.strptime(start, "%Y-%m-%d").date())
        if end:
            query = query.filter(Transaction.transaction_date <= datetime.strptime(end, "%Y-%m-%d").date())
    except ValueError:
        flash("Invalid date filter was ignored.", "warning")
    items = query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc()).all()
    return render_template("transactions.html", transactions=items, categories=CATEGORIES,
                           filters={"kind": kind, "category": category, "start": start, "end": end})

@transactions_bp.route("/transactions/add", methods=["GET", "POST"])
@login_required
def add_transaction():
    if request.method == "POST":
        try:
            kind, amount, category, description, tx_date = parse_transaction_form()
            db.session.add(Transaction(user_id=current_user.id, kind=kind, amount=amount,
                                       category=category, description=description,
                                       transaction_date=tx_date))
            db.session.commit()
            flash("Transaction added.", "success")
            return redirect(url_for("transactions.list_transactions"))
        except ValueError as exc:
            flash(str(exc), "danger")
    return render_template("transaction_form.html", categories=CATEGORIES, transaction=None)

@transactions_bp.route("/transactions/<int:tx_id>/edit", methods=["GET", "POST"])
@login_required
def edit_transaction(tx_id):
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()
    if request.method == "POST":
        try:
            tx.kind, tx.amount, tx.category, tx.description, tx.transaction_date = parse_transaction_form()
            db.session.commit()
            flash("Transaction updated.", "success")
            return redirect(url_for("transactions.list_transactions"))
        except ValueError as exc:
            flash(str(exc), "danger")
    return render_template("transaction_form.html", categories=CATEGORIES, transaction=tx)

@transactions_bp.route("/transactions/<int:tx_id>/delete", methods=["POST"])
@login_required
def delete_transaction(tx_id):
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()
    db.session.delete(tx)
    db.session.commit()
    flash("Transaction deleted.", "info")
    return redirect(url_for("transactions.list_transactions"))

@transactions_bp.route("/budget", methods=["POST"])
@login_required
def save_budget():
    month = request.form.get("month", "")
    try:
        datetime.strptime(month, "%Y-%m")
        amount = Decimal(request.form.get("amount", "0"))
        if amount <= 0:
            raise ValueError
    except (ValueError, InvalidOperation):
        flash("Enter a valid month and positive budget.", "danger")
        return redirect(url_for("transactions.dashboard"))
    budget = Budget.query.filter_by(user_id=current_user.id, month=month).first()
    if budget:
        budget.amount = amount
    else:
        db.session.add(Budget(user_id=current_user.id, month=month, amount=amount))
    db.session.commit()
    flash("Monthly budget saved.", "success")
    return redirect(url_for("transactions.dashboard", month=month))

@transactions_bp.route("/export")
@login_required
def export_csv():
    rows = Transaction.query.filter_by(user_id=current_user.id).order_by(
        Transaction.transaction_date.desc()).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Type", "Amount", "Category", "Description"])
    for tx in rows:
        writer.writerow([tx.transaction_date.isoformat(), tx.kind, str(tx.amount),
                         tx.category, tx.description])
    return Response(output.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=transactions.csv"})
