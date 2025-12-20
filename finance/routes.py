from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from finance.manager import FinanceManager
from finance.model import Income, Expense

#to keeps routes modular and clean
finance_bp = Blueprint("finance", __name__)
fm = FinanceManager()

@finance_bp.route("/", methods=["GET", "POST"])
def dashboard():
    month = request.args.get("month") or request.form.get("month")

    # Ensure month is always defined
    if not month:
        month = datetime.now().strftime("%Y-%m")

    if request.method == "POST":
        form_type = request.form.get("type")

        # for income transactions
        if form_type == "income":
            fm.add_transaction(Income(
            amount=float(request.form["amount"]),
            category=request.form["category"],
            date=request.form["date"],
            source=request.form["source"],
            recurring=bool(request.form.get("recurring")),
            description=request.form.get("description")
            ))


        # for expense transaction
        elif form_type == "expense":
            fm.add_transaction(Expense(
            amount=float(request.form["amount"]),
            category=request.form["category"],
            date=request.form["date"],
            payment_method=request.form["payment_method"],
            essential=bool(request.form.get("essential")),
            description=request.form.get("description")
            ))



        return redirect(url_for("finance.dashboard", month=month))

    summary_data = fm.get_monthly_summary(month)
    transactions_df = fm.get_transactions_table(month)

    # convert dataframe to html if exist
    table_html = (
        transactions_df.to_html(
            classes="table table-striped table-bordered",
            index=False
        ) if transactions_df is not None else None
    )

    return render_template("dashboard.html", summary=summary_data, table_html=table_html)