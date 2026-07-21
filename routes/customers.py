from flask import Blueprint, render_template, request, redirect, url_for
from database import get_connection

customers = Blueprint("customers", __name__)


@customers.route("/customers")
def view_customers():

    search = request.args.get("search", "")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if search:

        cursor.execute("""
            SELECT *
            FROM Customers
            WHERE CustomerName LIKE %s
            ORDER BY CustomerID DESC
        """, ("%" + search + "%",))

    else:

        cursor.execute("""
            SELECT *
            FROM Customers
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


@customers.route("/customers/add", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        name = request.form["customer_name"]
        phone = request.form["phone"]
        address = request.form["address"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Customers
            (CustomerName, Phone, Address)
            VALUES (%s,%s,%s)
        """, (name, phone, address))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("customers.view_customers"))

    return render_template("add_customer.html")


@customers.route("/customers/edit/<int:customer_id>", methods=["GET","POST"])
def edit_customer(customer_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        cursor.execute("""
            UPDATE Customers
            SET CustomerName=%s,
                Phone=%s,
                Address=%s
            WHERE CustomerID=%s
        """,(name,phone,address,customer_id))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("customers.view_customers"))

    cursor.execute("""
        SELECT *
        FROM Customers
        WHERE CustomerID=%s
    """,(customer_id,))

    customer = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_customer.html",
        customer=customer
    )


@customers.route("/customers/delete/<int:customer_id>")
def delete_customer(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM Customers
        WHERE CustomerID=%s
    """,(customer_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("customers.view_customers"))