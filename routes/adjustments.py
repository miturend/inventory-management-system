from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection
from utils.auth_helpers import admin_required
from utils.stock import add_stock_movement

adjustments = Blueprint("adjustments", __name__)


@adjustments.route("/stock/adjust/<int:product_id>", methods=["GET", "POST"])
@admin_required
def adjust_stock(product_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM products
        WHERE ProductID=%s
    """, (product_id,))

    product = cursor.fetchone()

    if request.method == "POST":

        adjustment = float(request.form["adjustment"])
        reason = request.form["reason"]

        cursor.execute("""
            UPDATE Products
            SET Stock = Stock + %s
            WHERE ProductID=%s
        """, (
            adjustment,
            product_id
        ))

        connection.commit()

        cursor.close()
        connection.close()

        add_stock_movement(
            product_id,
            "ADJUSTMENT",
            adjustment,
            reason
        )

        flash(
            "Stock adjusted successfully.",
            "success"
        )

        return redirect(
            url_for("products.view_products")
        )

    cursor.close()
    connection.close()

    return render_template(
        "adjust_stock.html",
        product=product
    )