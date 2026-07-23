from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection
from utils.auth_helpers import login_required, admin_required

customers = Blueprint("customers", __name__)


# ==========================
# View Customers
# ==========================
@customers.route("/customers")
@login_required
def view_customers():

    search = request.args.get("search", "")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if search:

        cursor.execute("""
            SELECT *
            FROM customers
            WHERE CustomerName LIKE %s
            ORDER BY CustomerID DESC
        """, ("%" + search + "%",))

    else:

        cursor.execute("""
            SELECT *
            FROM customers
            ORDER BY CustomerID DESC
        """)

    all_customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "customers.html",
        customers=all_customers,
        search=search
    )


# ==========================
# Add Customer
# ==========================
@customers.route("/customers/add", methods=["GET", "POST"])
@admin_required
def add_customer():

    if request.method == "POST":

        name = request.form["customer_name"]
        phone = request.form["phone"]
        address = request.form["address"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO customers
            (
                CustomerName,
                Phone,
                Address
            )
            VALUES
            (%s, %s, %s)
        """, (
            name,
            phone,
            address
        ))

        connection.commit()

        cursor.close()
        connection.close()

        flash("Customer added successfully.", "success")

        return redirect(url_for("customers.view_customers"))

    return render_template("add_customer.html")


# ==========================
# Edit Customer
# ==========================
@customers.route("/customers/edit/<int:customer_id>", methods=["GET", "POST"])
@admin_required
def edit_customer(customer_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["customer_name"]
        phone = request.form["phone"]
        address = request.form["address"]

        cursor.execute("""
            UPDATE customers
            SET
                CustomerName = %s,
                Phone = %s,
                Address = %s
            WHERE CustomerID = %s
        """, (
            name,
            phone,
            address,
            customer_id
        ))

        connection.commit()

        cursor.close()
        connection.close()

        flash("Customer updated successfully.", "success")

        return redirect(url_for("customers.view_customers"))

    cursor.execute("""
        SELECT *
        FROM customers
        WHERE CustomerID = %s
    """, (customer_id,))

    customer = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_customer.html",
        customer=customer
    )


# ==========================
# Delete Customer
# ==========================
@customers.route("/customers/delete/<int:customer_id>")
@admin_required
def delete_customer(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM customers
        WHERE CustomerID = %s
    """, (customer_id,))

    connection.commit()

    cursor.close()
    connection.close()

    flash("Customer deleted successfully.", "success")

    return redirect(url_for("customers.view_customers"))