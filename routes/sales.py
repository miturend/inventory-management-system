from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection
from mysql.connector import Error
from utils.stock import add_stock_movement
from utils.auth_helpers import login_required, admin_required

sales = Blueprint("sales", __name__)


# ==========================
# View Sales
# ==========================
@sales.route("/sales")
@login_required
def view_sales():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            Sales.SaleID,
            Customers.CustomerName,
            sales.SaleDate,
            Sales.Notes
        FROM sales
        INNER JOIN customers
            ON Sales.CustomerID = Customers.CustomerID
        ORDER BY Sales.SaleID DESC
    """)

    sales_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "sales.html",
        sales=sales_list
    )


# ==========================
# Add Sale
# ==========================
@sales.route("/sales/add", methods=["GET", "POST"])
@admin_required
def add_sale():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        customer = request.form["customer"]
        notes = request.form["notes"]

        cursor.execute("""
            INSERT INTO sales
            (
                CustomerID,
                SaleDate,
                Notes
            )
            VALUES
            (
                %s,
                CURDATE(),
                %s
            )
        """, (
            customer,
            notes
        ))

        connection.commit()

        cursor.close()
        connection.close()

        flash("Sale created successfully.", "success")

        return redirect(url_for("sales.view_sales"))

    cursor.execute("""
        SELECT *
        FROM customers
        ORDER BY CustomerName
    """)

    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "add_sale.html",
        customers=customers
    )


# ==========================
# View Sale Items
# ==========================
@sales.route("/sales/<int:sale_id>")
@login_required
def sale_items(sale_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            ProductID,
            ProductName
        FROM products
        ORDER BY ProductName
    """)

    products = cursor.fetchall()

    cursor.execute("""
        SELECT
            saleitems.SaleItemID,
            Products.ProductName,
            saleitems.Quantity,
            saleitems.UnitPrice,
            saleitems.TotalAmount
        FROM saleitems
        INNER JOIN products
            ON saleitems.ProductID = Products.ProductID
        WHERE saleitems.SaleID = %s
    """, (sale_id,))

    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "sale_items.html",
        sale_id=sale_id,
        products=products,
        items=items
    )


# ==========================
# Add Sale Item
# ==========================
@sales.route("/sales/<int:sale_id>/add_item", methods=["POST"])
@admin_required
def add_sale_item(sale_id):

    product = request.form["product"]
    quantity = float(request.form["quantity"])
    unit_price = float(request.form["unit_price"])

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO saleitems
            (
                SaleID,
                ProductID,
                Quantity,
                UnitPrice
            )
            VALUES
            (%s, %s, %s, %s)
        """, (
            sale_id,
            product,
            quantity,
            unit_price
        ))

        connection.commit()

        add_stock_movement(
        product,
        "SALE",
        -quantity,
        "Product sold"
)

        flash("Sale item added successfully.", "success")

    except Error:

        connection.rollback()

        flash("Not enough stock available.", "danger")

    finally:

        cursor.close()
        connection.close()

    return redirect(
        url_for(
            "sales.sale_items",
            sale_id=sale_id
        )
    )