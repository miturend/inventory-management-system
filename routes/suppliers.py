from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection
from utils.auth_helpers import login_required, admin_required

suppliers = Blueprint("suppliers", __name__)


# ==========================
# View Suppliers
# ==========================
@suppliers.route("/suppliers")
@login_required
def view_suppliers():

    search = request.args.get("search", "")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if search:

        cursor.execute("""
            SELECT *
            FROM suppliers
            WHERE SupplierName LIKE %s
            ORDER BY SupplierID DESC
        """, ("%" + search + "%",))

    else:

        cursor.execute("""
            SELECT *
            FROM suppliers
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


# ==========================
# Add Supplier
# ==========================
@suppliers.route("/suppliers/add", methods=["GET", "POST"])
@admin_required
def add_supplier():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO suppliers
            (
                SupplierName,
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

        flash("Supplier added successfully.", "success")

        return redirect(url_for("suppliers.view_suppliers"))

    return render_template("add_supplier.html")


# ==========================
# Edit Supplier
# ==========================
@suppliers.route("/suppliers/edit/<int:supplier_id>", methods=["GET", "POST"])
@admin_required
def edit_supplier(supplier_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        cursor.execute("""
            UPDATE suppliers
            SET
                SupplierName = %s,
                Phone = %s,
                Address = %s
            WHERE SupplierID = %s
        """, (
            name,
            phone,
            address,
            supplier_id
        ))

        connection.commit()

        cursor.close()
        connection.close()

        flash("Supplier updated successfully.", "success")

        return redirect(url_for("suppliers.view_suppliers"))

    cursor.execute("""
        SELECT *
        FROM suppliers
        WHERE SupplierID = %s
    """, (supplier_id,))

    supplier = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_supplier.html",
        supplier=supplier
    )


# ==========================
# Delete Supplier
# ==========================
@suppliers.route("/suppliers/delete/<int:supplier_id>")
@admin_required
def delete_supplier(supplier_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM suppliers
        WHERE SupplierID = %s
    """, (supplier_id,))

    connection.commit()

    cursor.close()
    connection.close()

    flash("Supplier deleted successfully.", "success")

    return redirect(url_for("suppliers.view_suppliers"))