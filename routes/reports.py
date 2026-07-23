from flask import Blueprint, render_template, request
from database import get_connection
from utils.auth_helpers import login_required

reports = Blueprint("reports", __name__)


@reports.route("/reports", methods=["GET", "POST"])
@login_required
def view_reports():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    sales = []
    total_sales = 0
    report_type = "sales"

    if request.method == "POST":

        report_type = request.form["report_type"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        # ==========================
        # SALES REPORT
        # ==========================
        if report_type == "sales":

            cursor.execute("""
                SELECT
                    sales.SaleDate,
                    Customers.CustomerName,
                    SUM(saleitems.TotalAmount) AS Total
                FROM sales
                INNER JOIN customers
                    ON Sales.CustomerID = Customers.CustomerID
                INNER JOIN saleitems
                    ON Sales.SaleID = saleitems.SaleID
                WHERE sales.SaleDate BETWEEN %s AND %s
                GROUP BY Sales.SaleID
                ORDER BY sales.SaleDate DESC
            """, (start_date, end_date))

            sales = cursor.fetchall()

            cursor.execute("""
                SELECT
                    IFNULL(SUM(saleitems.TotalAmount),0) AS total_sales
                FROM sales
                INNER JOIN saleitems
                    ON Sales.SaleID = saleitems.SaleID
                WHERE sales.SaleDate BETWEEN %s AND %s
            """, (start_date, end_date))

            total_sales = cursor.fetchone()["total_sales"]

        # ==========================
        # PURCHASE REPORT
        # ==========================
        elif report_type == "purchases":

            cursor.execute("""
                SELECT
                    Purchases.PurchaseDate AS SaleDate,
                    Suppliers.SupplierName AS CustomerName,
                    SUM(PurchaseItems.TotalAmount) AS Total
                FROM purchases
                INNER JOIN suppliers
                    ON Purchases.SupplierID = Suppliers.SupplierID
                INNER JOIN purchaseitems
                    ON Purchases.PurchaseID = PurchaseItems.PurchaseID
                WHERE Purchases.PurchaseDate BETWEEN %s AND %s
                GROUP BY Purchases.PurchaseID
                ORDER BY Purchases.PurchaseDate DESC
            """, (start_date, end_date))

            sales = cursor.fetchall()

            cursor.execute("""
                SELECT
                    IFNULL(SUM(PurchaseItems.TotalAmount),0) AS total_sales
                FROM purchases
                INNER JOIN purchaseitems
                    ON Purchases.PurchaseID = PurchaseItems.PurchaseID
                WHERE Purchases.PurchaseDate BETWEEN %s AND %s
            """, (start_date, end_date))

            total_sales = cursor.fetchone()["total_sales"]

        # ==========================
        # EXPENSE REPORT
        # ==========================
        elif report_type == "expenses":

            cursor.execute("""
                SELECT
                    ExpenseDate AS SaleDate,
                    Description AS CustomerName,
                    Amount AS Total
                FROM Expenses
                WHERE ExpenseDate BETWEEN %s AND %s
                ORDER BY ExpenseDate DESC
            """, (start_date, end_date))

            sales = cursor.fetchall()

            cursor.execute("""
                SELECT
                    IFNULL(SUM(Amount),0) AS total_sales
                FROM Expenses
                WHERE ExpenseDate BETWEEN %s AND %s
            """, (start_date, end_date))

            total_sales = cursor.fetchone()["total_sales"]

        elif report_type == "low_stock":

            cursor.execute("""
                SELECT
                    ProductName,
                    Stock
                FROM products
                WHERE Stock <= 10
                ORDER BY Stock ASC
            """)

            sales = cursor.fetchall()

            total_sales = 0

        # ==========================
        # PROFIT REPORT
        # ==========================
        elif report_type == "profit":

            # Total Sales
            cursor.execute("""
                SELECT IFNULL(SUM(saleitems.TotalAmount),0) AS sales
                FROM sales
                INNER JOIN saleitems
                    ON Sales.SaleID = saleitems.SaleID
                WHERE sales.SaleDate BETWEEN %s AND %s
            """, (start_date, end_date))

            total_sales_amount = cursor.fetchone()["sales"]

            # Total Purchases
            cursor.execute("""
                SELECT IFNULL(SUM(PurchaseItems.TotalAmount),0) AS purchases
                FROM purchases
                INNER JOIN purchaseitems
                    ON Purchases.PurchaseID = PurchaseItems.PurchaseID
                WHERE Purchases.PurchaseDate BETWEEN %s AND %s
            """, (start_date, end_date))

            total_purchase_amount = cursor.fetchone()["purchases"]

            # Total Expenses
            cursor.execute("""
                SELECT IFNULL(SUM(Amount),0) AS expenses
                FROM Expenses
                WHERE ExpenseDate BETWEEN %s AND %s
            """, (start_date, end_date))

            total_expense_amount = cursor.fetchone()["expenses"]

            profit = (
                total_sales_amount
                - total_purchase_amount
                - total_expense_amount
            )

            sales = [{
                "SaleDate": "",
                "CustomerName": "NET PROFIT",
                "Total": profit
            }]

            total_sales = profit

    cursor.close()
    connection.close()

    return render_template(
        "reports.html",
        sales=sales,
        total_sales=total_sales,
        report_type=report_type
    )