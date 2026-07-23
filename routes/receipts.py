from flask import Blueprint, render_template
from database import get_connection
from utils.auth_helpers import login_required
from flask import send_file
import tempfile
import os
from utils.pdf_receipt import generate_receipt

receipts = Blueprint("receipts", __name__)


@receipts.route("/receipt/<int:sale_id>")
@login_required
def sale_receipt(sale_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Receipt Header
    cursor.execute("""
        SELECT
            Sales.SaleID,
            sales.SaleDate,
            Sales.Notes,
            customers.CustomerName
        FROM sales
        INNER JOIN customers
            ON Sales.CustomerID = customers.CustomerID
        WHERE Sales.SaleID=%s
    """, (sale_id,))

    sale = cursor.fetchone()

    # Receipt Items
    cursor.execute("""
        SELECT
            products.ProductName,
            saleitems.Quantity,
            saleitems.UnitPrice,
            saleitems.TotalAmount
        FROM saleitems
        INNER JOIN products
            ON saleitems.ProductID=products.ProductID
        WHERE saleitems.SaleID=%s
    """, (sale_id,))

    items = cursor.fetchall()

    total = sum(item["TotalAmount"] for item in items)

    cursor.close()
    connection.close()

    return render_template(
        "receipt.html",
        sale=sale,
        items=items,
        total=total
    )

@receipts.route("/receipt/<int:sale_id>/pdf")
@login_required
def receipt_pdf(sale_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            Sales.SaleID,
            sales.SaleDate,
            Sales.Notes,
            customers.CustomerName
        FROM sales
        INNER JOIN customers
            ON Sales.CustomerID = customers.CustomerID
        WHERE Sales.SaleID=%s
    """, (sale_id,))

    sale = cursor.fetchone()

    cursor.execute("""
        SELECT
            products.ProductName,
            saleitems.Quantity,
            saleitems.UnitPrice,
            saleitems.TotalAmount
        FROM saleitems
        INNER JOIN products
            ON saleitems.ProductID=products.ProductID
        WHERE saleitems.SaleID=%s
    """, (sale_id,))

    items = cursor.fetchall()

    total = sum(item["TotalAmount"] for item in items)

    cursor.close()
    connection.close()

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp.close()

    generate_receipt(
        temp.name,
        sale,
        items,
        total
    )

    return send_file(
        temp.name,
        as_attachment=True,
        download_name=f"Receipt_{sale_id}.pdf"
    )    