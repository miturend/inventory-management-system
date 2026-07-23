from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection
from utils.auth_helpers import login_required
from utils.permissions import roles_required

settings = Blueprint("settings", __name__)


@settings.route("/settings", methods=["GET", "POST"])
@login_required
@roles_required("Admin")
def system_settings():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        business_name = request.form["business_name"]
        address = request.form["address"]
        phone = request.form["phone"]
        email = request.form["email"]
        currency = request.form["currency"]
        receipt_footer = request.form["receipt_footer"]
        low_stock = request.form["low_stock"]

        cursor.execute("""
            UPDATE Settings
            SET
                BusinessName = %s,
                BusinessAddress = %s,
                Phone = %s,
                Email = %s,
                CurrencySymbol = %s,
                ReceiptFooter = %s,
                LowStockThreshold = %s
            WHERE SettingID = 1
        """, (
            business_name,
            address,
            phone,
            email,
            currency,
            receipt_footer,
            low_stock
        ))

        connection.commit()

        flash("Settings updated successfully.", "success")

        cursor.close()
        connection.close()

        return redirect(url_for("settings.system_settings"))

    cursor.execute("SELECT * FROM Settings WHERE SettingID = 1")
    settings_data = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "settings.html",
        settings=settings_data
    )