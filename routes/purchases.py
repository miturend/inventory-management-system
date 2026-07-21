from flask import Blueprint, render_template, request, redirect, url_for
from database import get_connection

purchases = Blueprint("purchases", __name__)


@purchases.route("/purchases")
def view_purchases():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT

            Purchases.PurchaseID,
            Suppliers.SupplierName,
            Purchases.PurchaseDate,
            Purchases.InvoiceNumber,
            purchases.Notes AS notes

        FROM Purchases

        INNER JOIN Suppliers

        ON Purchases.SupplierID = Suppliers.SupplierID

        ORDER BY PurchaseID DESC

    """)

    purchase_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(

        "purchases.html",

        purchases=purchase_list

    )


@purchases.route("/purchases/add", methods=["GET", "POST"])
def add_purchase():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        supplier = request.form["supplier"]

        invoice = request.form["invoice"]

        notes = request.form["notes"]

        cursor.execute("""

            INSERT INTO Purchases

            (

                SupplierID,
                PurchaseDate,
                InvoiceNumber,
                Notes

            )

            VALUES

            (

                %s,
                CURDATE(),
                %s,
                %s

            )

        """, (

            supplier,
            invoice,
            notes

        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("purchases.view_purchases"))

    cursor.execute("""

        SELECT *

        FROM Suppliers

        ORDER BY SupplierName

    """)

    suppliers = cursor.fetchall()

    cursor.close()
    connection.close()
    

    return render_template(

        "add_purchase.html",

        suppliers=suppliers

    )
    #add new route
@purchases.route("/purchases/<int:purchase_id>")
def purchase_items(purchase_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM Products
        ORDER BY ProductName
    """)

    products = cursor.fetchall()

    print(products)

    cursor.execute("""
        SELECT
            PurchaseItems.PurchaseItemID,
            Products.ProductName,
            PurchaseItems.Quantity,
            PurchaseItems.UnitCost,
            PurchaseItems.TotalAmount
        FROM PurchaseItems
        INNER JOIN Products
        ON PurchaseItems.ProductID = Products.ProductID
        WHERE PurchaseItems.PurchaseID=%s
    """, (purchase_id,))

    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "purchase_items.html",
        purchase_id=purchase_id,
        products=products,
        items=items
    )    

    #add another route
@purchases.route("/purchases/<int:purchase_id>/add_item",
                 methods=["POST"])
def add_purchase_item(purchase_id):

    product = request.form["product"]
    quantity = int(request.form["quantity"])
    unit_cost = float(request.form["unit_cost"])

    total = quantity * unit_cost

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO PurchaseItems
    (
        PurchaseID,
        ProductID,
        Quantity,
        UnitCost
    )
    VALUES
    (%s, %s, %s, %s)
""", (
    purchase_id,
    product,
    quantity,
    unit_cost
))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(
        url_for(
            "purchases.purchase_items",
            purchase_id=purchase_id
        )
    )    