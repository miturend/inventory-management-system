from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection
from utils.auth_helpers import login_required, admin_required

expenses = Blueprint("expenses", __name__)


# ==========================
# View Expenses
# ==========================
@expenses.route("/expenses")
@login_required
def view_expenses():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM Expenses
        ORDER BY ExpenseID DESC
    """)

    expense_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "expenses.html",
        expenses=expense_list
    )


# ==========================
# Add Expense
# ==========================
@expenses.route("/expenses/add", methods=["GET", "POST"])
@admin_required
def add_expense():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        description = request.form["description"]
        category = request.form["category"]
        amount = request.form["amount"]

        cursor.execute("""
            INSERT INTO Expenses
            (
                ExpenseDate,
                Description,
                Category,
                Amount
            )
            VALUES
            (
                CURDATE(),
                %s,
                %s,
                %s
            )
        """, (
            description,
            category,
            amount
        ))

        connection.commit()

        cursor.close()
        connection.close()

        flash("Expense added successfully.", "success")

        return redirect(
            url_for("expenses.view_expenses")
        )

    cursor.close()
    connection.close()

    return render_template(
        "add_expense.html"
    )