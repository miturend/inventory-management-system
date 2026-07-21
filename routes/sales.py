from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection
from mysql.connector import Error

sales = Blueprint("sales", __name__)

@sales.route("/sales")
def view_sales():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            Sales.SaleID,
            Customers.CustomerName,
            Sales.SaleDate,
            Sales.Notes
        FROM Sales
        INNER JOIN Customers
        ON Sales.CustomerID = Customers.CustomerID
        ORDER BY SaleID DESC
    """)

    sales_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "sales.html",
        sales=sales_list
    )

    #add new route(New sale feature)


# ... keep your existing code ...

@sales.route("/sales/add", methods=["GET", "POST"])
def add_sale():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        customer = request.form["customer"]
        notes = request.form["notes"]

        cursor.execute("""
            INSERT INTO Sales
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
        """, (customer, notes))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("sales.view_sales"))

    cursor.execute("""
        SELECT *
        FROM Customers
        ORDER BY CustomerName
    """)

    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "add_sale.html",
        customers=customers
    )    

    #add route fro salesitems
@sales.route("/sales/<int:sale_id>/add_item", methods=["POST"])
def add_sale_item(sale_id):

    product = request.form["product"]
    quantity = float(request.form["quantity"])
    unit_price = float(request.form["unit_price"])

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO SaleItems
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

    except Error as e:

        connection.rollback()

        cursor.close()
        connection.close()

        flash("Not enough stock available.", "danger")

        return redirect(
            url_for(
                "sales.sale_items",
                sale_id=sale_id
            )
    )

    cursor.close()
    connection.close()

    return redirect(
        url_for(
            "sales.sale_items",
            sale_id=sale_id
        )
    )

@sales.route("/sales/<int:sale_id>")
def sale_items(sale_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            productid,
            productname
        FROM Products
        ORDER BY productname
    """)

    products = cursor.fetchall()

    cursor.execute("""
        SELECT
            SaleItems.SaleItemID,
            Products.productname,
            SaleItems.Quantity,
            SaleItems.UnitPrice,
            SaleItems.TotalAmount
        FROM SaleItems
        INNER JOIN Products
        ON SaleItems.ProductID = Products.productid
        WHERE SaleItems.SaleID = %s
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