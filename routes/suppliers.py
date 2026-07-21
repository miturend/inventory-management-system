from flask import Blueprint, render_template, request, redirect, url_for
from database import get_connection

suppliers = Blueprint("suppliers", __name__)


@suppliers.route("/suppliers")
def view_suppliers():

    search = request.args.get("search", "")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if search:

        cursor.execute("""
            SELECT *
            FROM Suppliers
            WHERE SupplierName LIKE %s
            ORDER BY SupplierID DESC
        """, ("%" + search + "%",))

    else:

        cursor.execute("""
            SELECT *
            FROM Suppliers
            ORDER BY SupplierID DESC
        """)

    all_suppliers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "suppliers.html",
        suppliers=all_suppliers,
        search=search
    )


@suppliers.route("/suppliers/add", methods=["GET", "POST"])
def add_supplier():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Suppliers
            (SupplierName, Phone, Address)
            VALUES (%s,%s,%s)
        """, (name, phone, address))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("suppliers.view_suppliers"))

    return render_template("add_supplier.html")


@suppliers.route("/suppliers/edit/<int:supplier_id>", methods=["GET","POST"])
def edit_supplier(supplier_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        cursor.execute("""
            UPDATE Suppliers
            SET SupplierName=%s,
                Phone=%s,
                Address=%s
            WHERE SupplierID=%s
        """, (name, phone, address, supplier_id))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("suppliers.view_suppliers"))

    cursor.execute("""
        SELECT *
        FROM Suppliers
        WHERE SupplierID=%s
    """, (supplier_id,))

    supplier = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_supplier.html",
        supplier=supplier
    )


@suppliers.route("/suppliers/delete/<int:supplier_id>")
def delete_supplier(supplier_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM Suppliers
        WHERE SupplierID=%s
    """, (supplier_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("suppliers.view_suppliers"))