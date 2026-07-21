from flask import Blueprint, render_template, request, redirect, url_for
from database import get_connection

products = Blueprint("products", __name__)


# View all products
@products.route("/products")
def view_products():

    search = request.args.get("search", "")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if search:

        cursor.execute("""
            SELECT ProductID,
                   ProductName,
                   SellingPrice,
                   Stock
            FROM Products
            WHERE ProductName LIKE %s
            ORDER BY ProductID DESC
        """, ("%" + search + "%",))

    else:

        cursor.execute("""
            SELECT ProductID,
                   ProductName,
                   SellingPrice,
                   Stock
            FROM Products
            ORDER BY ProductID DESC
        """)

    all_products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "products.html",
        products=all_products,
        search=search
    )


# Add a new product
@products.route("/products/add", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        product_name = request.form["product_name"]
        selling_price = request.form["selling_price"]
        stock = request.form["stock"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Products
            (ProductName, SellingPrice, Stock)
            VALUES (%s, %s, %s)
        """, (product_name, selling_price, stock))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("products.view_products"))

    return render_template("add_product.html")

#edit Product
@products.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        product_name = request.form["product_name"]
        selling_price = request.form["selling_price"]
        stock = request.form["stock"]

        cursor.execute("""
            UPDATE Products
            SET ProductName = %s,
                SellingPrice = %s,
                Stock = %s
            WHERE ProductID = %s
        """, (product_name, selling_price, stock, product_id))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("products.view_products"))

    cursor.execute("""
        SELECT *
        FROM Products
        WHERE ProductID = %s
    """, (product_id,))

    product = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_product.html",
        product=product
    )

    #Delete Product

@products.route("/products/delete/<int:product_id>")
def delete_product(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM Products
        WHERE ProductID = %s
    """, (product_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("products.view_products"))