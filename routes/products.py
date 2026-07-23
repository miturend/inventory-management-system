from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection
from utils.auth_helpers import login_required
from utils.permissions import roles_required
from utils.activity import log_activity

products = Blueprint("products", __name__)


# ==========================
# View Products
# ==========================
@products.route("/products")
@login_required
def view_products():

    search = request.args.get("search", "")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if search:

        cursor.execute("""
            SELECT
                ProductID,
                ProductName,
                SellingPrice,
                Stock
            FROM products
            WHERE ProductName LIKE %s
            ORDER BY ProductID DESC
        """, ("%" + search + "%",))

    else:

        cursor.execute("""
            SELECT
                ProductID,
                ProductName,
                SellingPrice,
                Stock
            FROM products
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


# ==========================
# Add Product
# ==========================
@products.route("/products/add", methods=["GET", "POST"])
@login_required
@roles_required("Admin","Manager")
def add_product():

    if request.method == "POST":

        product_name = request.form["product_name"]
        selling_price = request.form["selling_price"]
        stock = request.form["stock"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO products
            (
                ProductName,
                SellingPrice,
                Stock
            )
            VALUES
            (%s, %s, %s)
        """, (
            product_name,
            selling_price,
            stock
        ))

        connection.commit()

        cursor.close()
        connection.close()

        log_activity(
            "ADD PRODUCT",
            f"Added product: {product_name}"
        )

        flash("Product added successfully.", "success")

        return redirect(url_for("products.view_products"))

    return render_template("add_product.html")


# ==========================
# Edit Product
# ==========================
@products.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
@roles_required("Admin","Manager")
def edit_product(product_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        product_name = request.form["product_name"]
        selling_price = request.form["selling_price"]
        stock = request.form["stock"]

        cursor.execute("""
            UPDATE products
            SET
                ProductName = %s,
                SellingPrice = %s,
                Stock = %s
            WHERE ProductID = %s
        """, (
            product_name,
            selling_price,
            stock,
            product_id
        ))

        connection.commit()

        cursor.close()
        connection.close()

        log_activity(
            "EDIT PRODUCT",
            f"Updated product: {product_name}"
        )

        flash("Product updated successfully.", "success")

        return redirect(url_for("products.view_products"))

    cursor.execute("""
        SELECT *
        FROM products
        WHERE ProductID = %s
    """, (product_id,))

    product = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_product.html",
        product=product
    )


# ==========================
# Delete Product
# ==========================
@products.route("/products/delete/<int:product_id>")
@login_required
@roles_required("Admin")
def delete_product(product_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    cursor.execute("""
        SELECT ProductName
        FROM products
        WHERE ProductID = %s
    """, (product_id,))


    product = cursor.fetchone()


    cursor.execute("""
        DELETE FROM products
        WHERE ProductID = %s
    """, (product_id,))


    connection.commit()

    cursor.close()
    connection.close()


    log_activity(
        "DELETE PRODUCT",
        f"Deleted product: {product['ProductName']}"
    )


    flash("Product deleted successfully.", "success")


    return redirect(url_for("products.view_products"))